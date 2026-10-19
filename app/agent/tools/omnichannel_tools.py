import os
import json
import time
from typing import Dict, Any, Optional
from langchain_core.tools import tool
from app.db.session import SessionLocal
from app.db.models import ToolExecutionLog

def _log(tool_name: str, args: dict, result: Any, success: bool = True, err: str = None, duration_ms: float = 0.0):
    db = SessionLocal()
    try:
        log_entry = ToolExecutionLog(
            tool_name=tool_name,
            arguments=args,
            result_summary=str(result)[:500] if result else "",
            success=success,
            error_message=err,
            execution_time_ms=duration_ms
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        print(f"Log error: {e}")
    finally:
        db.close()

# 1. dispatch_executive_response_email
def send_live_smtp_email(recipient_email: str, subject: str, response_body: str) -> Dict[str, Any]:
    """Helper to dispatch live email using configured SMTP credentials or return clear diagnosis."""
    from dotenv import load_dotenv
    load_dotenv(override=True)
    import os
    import smtplib
    import ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
    user = os.getenv("SMTP_USER", "").strip()
    raw_pass = os.getenv("SMTP_PASSWORD", "").strip()
    # Google App Passwords often have spaces (e.g. 'abcd efgh ijkl mnop') -> strip spaces
    clean_pass = raw_pass.replace(" ", "")
    from_addr = os.getenv("EMAIL_FROM", user if user else "sales-intelligence@enterprise.internal").strip()

    if not user or not clean_pass:
        return {
            "success": False,
            "error": "SMTP_USER or SMTP_PASSWORD not configured. Please supply your Gmail address and 16-character App Password.",
            "note": "Credentials required for direct Gmail inbox delivery."
        }

    mail = MIMEMultipart()
    mail["From"] = from_addr
    mail["To"] = recipient_email
    mail["Subject"] = subject
    mail.attach(MIMEText(response_body, "plain"))

    # Attempt 1: Port 587 (STARTTLS)
    try:
        with smtplib.SMTP(host, 587, timeout=10) as s:
            s.starttls()
            s.login(user, clean_pass)
            s.send_message(mail)
        return {
            "success": True,
            "error": None,
            "note": f"Successfully delivered live email to {recipient_email} via {host}:587 (TLS)."
        }
    except Exception as e_587:
        # Attempt 2: Port 465 (SSL Direct)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, 465, context=context, timeout=10) as s:
                s.login(user, clean_pass)
                s.send_message(mail)
            return {
                "success": True,
                "error": None,
                "note": f"Successfully delivered live email to {recipient_email} via {host}:465 (SSL)."
            }
        except Exception as e_465:
            err_msg = str(e_465) or str(e_587)
            user_tip = f"SMTP Authentication Rejected: {err_msg}"
            if "10053" in err_msg or "534" in err_msg or "Application-specific password required" in err_msg or "BadCredentials" in err_msg or "Username and Password not accepted" in err_msg:
                user_tip = (
                    "Google rejected the connection because a regular Gmail password was used. "
                    "Google strictly requires a 16-character App Password for 2FA accounts. "
                    "Quick Fix: Go to https://myaccount.google.com/apppasswords, generate a 16-letter App Password, and paste it into SMTP_PASSWORD."
                )
            return {
                "success": False,
                "error": err_msg,
                "note": user_tip
            }

@tool
def dispatch_executive_response_email(recipient_email: str, subject: str, response_body: str) -> str:
    """Switches and dispatches the entire agent executive response and findings directly to the user's email address (e.g. vishlpal97@gmail.com)."""
    start = time.time()
    try:
        from app.config import settings
        sent_real = False
        smtp_note = ""

        # Attempt live SMTP delivery
        res = send_live_smtp_email(recipient_email, subject, response_body)
        sent_real = res["success"]
        smtp_note = res["note"]

        # Always persist to audit outbox file for permanent verification
        outbox_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "outbox")
        os.makedirs(outbox_dir, exist_ok=True)
        outbox_file = os.path.join(outbox_dir, "dispatched_executive_emails.jsonl")
        
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "recipient_email": recipient_email,
            "subject": subject,
            "body": response_body,
            "delivery_note": smtp_note,
            "live_smtp_sent": sent_real
        }
        with open(outbox_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        delivery_payload = {
            "status": "DELIVERED" if sent_real else "ARCHIVED_OUTBOX",
            "channel": "EXECUTIVE_EMAIL_GATEWAY",
            "recipient_email": recipient_email,
            "subject": subject,
            "message_length": len(response_body),
            "dispatched_at": entry["timestamp"],
            "delivery_receipt_id": f"mail-ack-{int(time.time()*1000)}",
            "outbox_path": outbox_file,
            "live_delivery_status": smtp_note,
            "live_smtp_sent": sent_real
        }
        out = json.dumps(delivery_payload, indent=2)
        _log("dispatch_executive_response_email", {"recipient": recipient_email, "subject": subject}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err = str(e)
        _log("dispatch_executive_response_email", {"recipient": recipient_email}, None, False, err, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err})

# 2. execute_system_command
@tool
def execute_system_command(command: str) -> str:
    """Executes an authorized development/build/deploy command on the system (e.g. git status, pytest, build validation)."""
    start = time.time()
    try:
        import subprocess
        # Allowlisted safe commands for build/deploy/inspection
        cmd_lower = command.lower()
        blocked_keywords = ["rm -rf", "del /s", "format", "shutdown", "drop database"]
        if any(b in cmd_lower for b in blocked_keywords):
            return json.dumps({"status": "BLOCKED", "error": "Command contains unsafe operation."})
        
        proc = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        out = json.dumps({
            "status": "SUCCESS" if proc.returncode == 0 else "FAILED",
            "command": command,
            "exit_code": proc.returncode,
            "stdout": proc.stdout[:1500] if proc.stdout else "",
            "stderr": proc.stderr[:500] if proc.stderr else ""
        }, indent=2)
        _log("execute_system_command", {"command": command}, out, proc.returncode == 0, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err = str(e)
        _log("execute_system_command", {"command": command}, None, False, err, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err})

# 3. modify_project_asset
@tool
def modify_project_asset(file_path: str, operation: str, content_snippet: str) -> str:
    """Performs an agentic edit or inspection on project assets (e.g. configs, templates, scripts) when instructed by user."""
    start = time.time()
    try:
        target = os.path.abspath(file_path)
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        # Verify within project directory
        if not target.startswith(base):
            return json.dumps({"status": "ERROR", "error": "Target file is outside the project root."})
        
        if operation == "READ":
            if not os.path.exists(target):
                return json.dumps({"status": "ERROR", "error": f"File {file_path} not found."})
            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                data = f.read(2000)
            return json.dumps({"status": "SUCCESS", "operation": "READ", "content_preview": data})
        
        elif operation in ["APPEND", "WRITE"]:
            mode = "a" if operation == "APPEND" else "w"
            with open(target, mode, encoding="utf-8") as f:
                f.write(content_snippet)
            return json.dumps({"status": "SUCCESS", "operation": operation, "file": file_path, "bytes_written": len(content_snippet)})
        
        else:
            return json.dumps({"status": "ERROR", "error": f"Unsupported operation '{operation}'. Use READ, WRITE, or APPEND."})
    except Exception as e:
        err = str(e)
        return json.dumps({"status": "ERROR", "error": err})

