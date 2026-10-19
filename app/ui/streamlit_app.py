import streamlit as st
import pandas as pd
import requests
import json
import time
import os
from dotenv import load_dotenv

# Always reload environment variables on every rerun
load_dotenv(override=True)

st.set_page_config(
    page_title="Enterprise AI Workforce — Multi-Agent OS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Corporate Design (Tailwind / Slate Light Theme — No radiant/purple/black-white)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & Palette */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    /* Clean Slate Light Canvas */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* Hide Streamlit Chrome */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}

    /* Top Enterprise App Bar */
    .corp-header-bar {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 16px 24px;
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .corp-brand-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.015em;
    }
    .corp-brand-sub {
        font-size: 0.82rem;
        color: #475569;
        margin-top: 3px;
    }
    .badge-runtime-on {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-runtime-off {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Enterprise Surface Cards */
    .corp-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    /* Executive Briefing Report Frame */
    .executive-briefing-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #1e3a8a;
        border-radius: 6px;
        padding: 24px;
        margin-top: 18px;
        margin-bottom: 22px;
        color: #0f172a;
        line-height: 1.65;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }

    /* Metric cards styling */
    .metric-row {
        display: flex;
        gap: 16px;
        margin-bottom: 16px;
    }
    .metric-chip {
        flex: 1;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 12px 16px;
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }
    .metric-val {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 2px;
    }

    /* Outbox item box */
    .outbox-item {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 14px 18px;
        margin-top: 8px;
        margin-bottom: 12px;
    }

    /* Streamlit input refinement */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
        border-radius: 5px !important;
    }
    .stButton>button {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border: 1px solid #172554 !important;
        border-radius: 5px !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        transition: background-color 0.15s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #1d4ed8 !important;
        border-color: #1e40af !important;
    }
</style>
""", unsafe_allow_html=True)

API_BASE = "http://127.0.0.1:8000"

def get_backend_health():
    try:
        r = requests.get(f"{API_BASE}/health", timeout=1.5)
        return r.status_code == 200, r.json() if r.status_code == 200 else {}
    except Exception:
        return False, {}

online, h_data = get_backend_health()

# Top Corporate Header
st.markdown(f"""
<div class="corp-header-bar">
    <div>
        <div class="corp-brand-title">Enterprise AI Workforce — Multi-Agent Operating System</div>
        <div class="corp-brand-sub">Autonomous Decision Runtime | Sales Intelligence & Regional Sourcing Agent</div>
    </div>
    <div>
        <span class="{"badge-runtime-on" if online else "badge-runtime-off"}">
            {"● FastAPI Runtime: Connected (Port 8000)" if online else "○ FastAPI Runtime: Offline"}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("### Enterprise Navigation")
section = st.sidebar.radio(
    "Workspaces",
    [
        "Sales Intelligence Agent Console",
        "Executive Email Relay & Gateway",
        "Client Communication Handler",
        "AdventureWorks Dataset Explorer",
        "Predictive Account Valuation"
    ],
    key="nav_radio_section"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**System Architecture**
- **Core Agent**: Sales Intelligence
- **Enterprise DB**: MS AdventureWorks
- **Government Benchmark**: ASI Open-Data
- **Delivery Destination**: `vishlpal97@gmail.com`
- **Execution Engine**: Scikit-Learn + LangChain
""")

# =================================================================================================
# View 1: Sales Intelligence Agent Console
# =================================================================================================
if section == "Sales Intelligence Agent Console":
    st.markdown("#### Autonomous Sales Intelligence Console")
    st.caption("Submit natural language sales directives. The agent reasons dynamically, invokes verified database tools against Microsoft AdventureWorks records, persists opportunities, and routes the report to vishlpal97@gmail.com.")

    c_left, c_right = st.columns([3, 1])
    with c_left:
        template = st.selectbox(
            "Select an enterprise directive template or enter custom instructions:",
            [
                "Analyze our sales for the latest available year 2024. Identify our top five products, find regions with declining sales, and recommend three business opportunities.",
                "Inspect AdventureWorks enterprise accounts across Maharashtra and Gujarat, assess spending distribution, and identify top priority opportunities.",
                "Evaluate low-margin regional performance in Tamil Nadu and Uttar Pradesh and generate strategic turnaround recommendations.",
                "Custom Executive Directive..."
            ],
            key="sales_template_selector"
        )
        task_val = "" if template == "Custom Executive Directive..." else template
        objective_text = st.text_area("Objective Directive:", value=task_val, height=95, key="sales_objective_input")

    with c_right:
        st.markdown("**Execution Safeguards**")
        max_steps = st.number_input("Max Reasoning Steps", min_value=2, max_value=12, value=6, key="sales_max_steps")
        email_dest = st.text_input("Executive Report Recipient:", value="vishlpal97@gmail.com", disabled=True, key="sales_email_dest")
        st.caption("Directly routes to recipient.")
        st.write("")
        exec_btn = st.button("Execute Directive", type="primary", use_container_width=True, key="sales_exec_btn")

    if exec_btn:
        if not objective_text.strip():
            st.warning("Please provide a valid enterprise directive.")
        else:
            with st.status("Autonomous Agent Operating Loop Running...", expanded=True) as status_box:
                st.write("Initializing agent session and tool bindings...")
                
                # Guaranteed Self-Healing Execution Loop
                max_retries = 3
                success = False
                res_data = None
                start_exec = time.time()
                
                for attempt in range(1, max_retries + 1):
                    try:
                        st.write(f"Executing reasoning loop (Pass {attempt}/{max_retries})...")
                        payload = {
                            "objective": objective_text.strip(),
                            "max_steps": max_steps
                        }
                        resp = requests.post(f"{API_BASE}/agent/run", json=payload, timeout=90)
                        if resp.status_code == 200:
                            res_data = resp.json()
                            if res_data.get("status") in ["COMPLETED", "SUCCESS"]:
                                success = True
                                break
                    except Exception as err:
                        st.write(f"Transient fault on pass {attempt}: {err}. Retrying in loop...")
                        time.sleep(1)

                exec_duration = round(time.time() - start_exec, 2)

                if success and res_data:
                    status_box.update(label=f"Workflow Successfully Completed in {exec_duration}s", state="complete")
                    
                    st.markdown("---")
                    
                    # Enterprise Summary Metrics
                    st.markdown(f"""
                    <div class="metric-row">
                        <div class="metric-chip">
                            <div class="metric-label">Execution Status</div>
                            <div class="metric-val" style="color: #047857;">{res_data.get("status", "COMPLETED")}</div>
                        </div>
                        <div class="metric-chip">
                            <div class="metric-label">Tools Executed</div>
                            <div class="metric-val">{res_data.get("executed_tools_count", 0)}</div>
                        </div>
                        <div class="metric-chip">
                            <div class="metric-label">Execution Latency</div>
                            <div class="metric-val">{exec_duration}s</div>
                        </div>
                        <div class="metric-chip">
                            <div class="metric-label">Report Dispatched To</div>
                            <div class="metric-val" style="font-size: 0.95rem; padding-top: 4px;">vishlpal97@gmail.com</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Distinct Executive Briefing Box
                    st.markdown("#### Executive Briefing & Strategic Findings")
                    st.markdown("""<div class="executive-briefing-box">""", unsafe_allow_html=True)
                    st.markdown(res_data.get("final_response", "No report content generated."))
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Delivery Confirmation
                    st.success("Report delivered to executive relay for vishlpal97@gmail.com. Check 'Executive Email Relay & Gateway' workspace to inspect live SMTP delivery status.")

                    # Audit Trail & Execution Timeline
                    with st.expander("Audit Trail — Recorded Autonomous Tool Execution Events"):
                        for ev in res_data.get("events", []):
                            st.write(f"• **Step {ev['step']} [{ev['event_type']}]**: {ev['description']}")
                            if ev.get("metadata"):
                                st.json(ev["metadata"])
                else:
                    status_box.update(label="Execution Fault", state="error")
                    st.error("The agent could not complete the directive after multiple attempts. Inspect backend logs.")

# =================================================================================================
# View 2: Executive Email Relay & Gateway
# =================================================================================================
elif section == "Executive Email Relay & Gateway":
    st.markdown("#### Executive Email Relay & Live Delivery Gateway")
    st.caption("Manage live SMTP relay configuration to deliver reports directly to vishlpal97@gmail.com and inspect dispatched enterprise logs.")

    from app.agent.tools.omnichannel_tools import send_live_smtp_email

    cur_smtp_user = os.getenv("SMTP_USER", "").strip()
    cur_smtp_pass = os.getenv("SMTP_PASSWORD", "").strip()
    cur_smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
    cur_smtp_port = int(os.getenv("SMTP_PORT", "587"))

    col_smtp1, col_smtp2 = st.columns([1, 1])

    with col_smtp1:
        st.markdown("##### Live SMTP Relay Configuration")
        smtp_configured = bool(cur_smtp_user and cur_smtp_pass)

        if smtp_configured:
            st.success(f"● Live SMTP Relay Active ({cur_smtp_host}:{cur_smtp_port}) | Sender: {cur_smtp_user}")
        else:
            st.warning("○ Live SMTP Inactive: Reports are currently saved to the verified enterprise outbox on disk. Configure Gmail credentials below to receive live emails in your inbox.")

        with st.form("smtp_config_form"):
            st.write("**Configure Google / SMTP Relay Credentials:**")
            new_smtp_user = st.text_input("Sender Gmail Address:", value=cur_smtp_user or "vishlpal97@gmail.com", key="form_smtp_user")
            new_smtp_pass = st.text_input("Google App Password (16 characters):", value=cur_smtp_pass, type="password", help="Generate via Google Account -> Security -> 2-Step Verification -> App Passwords", key="form_smtp_pass")
            new_smtp_host = st.text_input("SMTP Host:", value=cur_smtp_host, key="form_smtp_host")
            new_smtp_port = st.number_input("SMTP Port:", value=cur_smtp_port, key="form_smtp_port")
            save_smtp_btn = st.form_submit_button("Save Credentials to .env")

            if save_smtp_btn:
                env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
                env_lines = []
                if os.path.exists(env_path):
                    with open(env_path, "r", encoding="utf-8") as f:
                        env_lines = f.readlines()
                
                key_map = {
                    "SMTP_HOST": new_smtp_host.strip(),
                    "SMTP_PORT": str(new_smtp_port),
                    "SMTP_USER": new_smtp_user.strip(),
                    "SMTP_PASSWORD": new_smtp_pass.strip(),
                    "EMAIL_FROM": new_smtp_user.strip(),
                    "EMAIL_PROVIDER": "smtp"
                }
                updated_keys = set()
                new_file_lines = []
                for line in env_lines:
                    k = line.split("=")[0].strip() if "=" in line else ""
                    if k in key_map:
                        new_file_lines.append(f"{k}={key_map[k]}\n")
                        updated_keys.add(k)
                    else:
                        new_file_lines.append(line)
                for k, v in key_map.items():
                    if k not in updated_keys:
                        new_file_lines.append(f"{k}={v}\n")

                with open(env_path, "w", encoding="utf-8") as f:
                    f.writelines(new_file_lines)

                # Immediately update runtime environment variables
                for k, v in key_map.items():
                    os.environ[k] = v

                st.success("Credentials saved to .env and applied immediately! You can now test live delivery.")
                time.sleep(0.5)
                st.rerun()

    with col_smtp2:
        st.markdown("##### Test Live Delivery to vishlpal97@gmail.com")
        st.write("Send a live verification test email to verify socket handshake and authentication.")
        
        test_sub = st.text_input("Test Subject:", value="Enterprise AI OS: Live Delivery Verification", key="live_test_sub")
        test_body = st.text_area("Test Body:", value="This is an automated verification test from Enterprise Multi-Agent OS confirming email relay delivery to vishlpal97@gmail.com.", height=85, key="live_test_body")
        
        test_btn = st.button("Dispatch Live Test Email", type="primary", key="live_test_dispatch_btn")
        if test_btn:
            if not cur_smtp_user or not cur_smtp_pass:
                st.warning("⚠️ Credentials Required: Please enter your Gmail address and 16-character App Password on the left and click 'Save Credentials to .env' before dispatching a live test.")
            else:
                with st.spinner("Connecting to SMTP server..."):
                    test_res = send_live_smtp_email("vishlpal97@gmail.com", test_sub, test_body)
                    if test_res["success"]:
                        st.success(f"Delivered! {test_res['note']}")
                    else:
                        st.error(f"Delivery Failed: {test_res['error']}\n\nNote: {test_res['note']}")

    st.markdown("---")
    st.markdown("##### Dispatched Reports & Outbox History")
    outbox_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "outbox", "dispatched_executive_emails.jsonl")
    if os.path.exists(outbox_file):
        records = []
        with open(outbox_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        if records:
            st.write(f"Total Dispatched Messages: **{len(records)}**")
            for idx, r in enumerate(reversed(records[-10:])):
                with st.expander(f"✉️ {r.get('subject', 'Report')} | Recipient: {r.get('recipient_email', 'vishlpal97@gmail.com')} | {r.get('timestamp', '')}"):
                    st.write(f"**Relay Note:** {r.get('delivery_note', 'Archived')}")
                    st.write(f"**Live SMTP Sent:** `{r.get('live_smtp_sent', False)}`")
                    st.markdown("**Message Content:**")
                    st.markdown(r.get("body", "*(Empty message)*"))
        else:
            st.info("Outbox is empty.")
    else:
        st.info("No dispatched emails in outbox yet.")

# =================================================================================================
# View 3: Client Communication Handler
# =================================================================================================
elif section == "Client Communication Handler":
    st.markdown("#### Inbound Prospect Communications & Intent Classifier")
    st.caption("Classifies inbound inquiries from enterprise prospects, detects sentiment, and generates recommended actions.")

    from app.agent.tools.sales_tools import analyze_incoming_customer_reply, execute_autonomous_sales_action

    c1, c2 = st.columns(2)
    with c1:
        account_select = st.selectbox(
            "Target Account:",
            [
                "kavita.patel@westernprecision.in | Western Precision Components",
                "rajesh.sharma@apex-mfg.in | Apex Manufacturing Ltd",
                "manoj.hegde@deccanelec.in | Deccan Electronics Infra"
            ],
            key="client_account_select"
        )
        c_mail = account_select.split("|")[0].strip()
    with c2:
        inbound_preset = st.selectbox(
            "Preset Inbound Client Inquiry:",
            [
                "We reviewed your supply-chain optimization pitch. Can we schedule a 15-minute briefing this Thursday at 2 PM?",
                "Could you send us the official price schedule and tiered quote for our Ahmedabad manufacturing unit?",
                "We do not have budget for new software this quarter. Please remove us from your list."
            ],
            key="client_preset_select"
        )

    msg_input = st.text_area("Client Message Content:", value=inbound_preset, height=90, key="client_msg_input")

    if st.button("Analyze Inbound Message", type="primary", key="client_analyze_btn"):
        res = analyze_incoming_customer_reply.invoke({"customer_email": c_mail, "reply_text": msg_input})
        data = json.loads(res)

        st.markdown("---")
        st.markdown("##### Classification & Recommended Action")
        col_a, col_b = st.columns(2)
        with col_a:
            st.write(f"**Detected Intent:** `{data['detected_intent']}`")
            st.write(f"**Sentiment Analysis:** `{data['sentiment']}`")
        with col_b:
            st.write(f"**Autonomous Action Recommendation:** `{data['autonomous_recommended_action']}`")

        st.info(f"**Drafted Contextual Response:**\n\n{data['suggested_response_draft']}")

        if st.button(f"Approve & Execute '{data['autonomous_recommended_action']}'", key="client_approve_btn"):
            act_res = execute_autonomous_sales_action.invoke({
                "customer_email": c_mail,
                "action_type": data["autonomous_recommended_action"],
                "action_summary": f"Executed automated next step '{data['autonomous_recommended_action']}'"
            })
            st.success("Action logged to relational audit records.")

# =================================================================================================
# View 4: AdventureWorks Dataset Explorer
# =================================================================================================
elif section == "AdventureWorks Dataset Explorer":
    st.markdown("#### Microsoft AdventureWorks OLTP Database Explorer")
    st.caption("Verified enterprise tables backing deterministic sales analytics.")

    from app.services.baseline_analytics import RAW_DIR

    tab1, tab2, tab3 = st.tabs(["Sales Orders Header", "Sales Order Line Details", "Customer Accounts"])
    with tab1:
        df_ord = pd.read_csv(os.path.join(RAW_DIR, "adventureworks_sales_orders.csv"))
        st.dataframe(df_ord, use_container_width=True)
    with tab2:
        df_det = pd.read_csv(os.path.join(RAW_DIR, "adventureworks_order_details.csv"))
        st.dataframe(df_det, use_container_width=True)
    with tab3:
        df_cust = pd.read_csv(os.path.join(RAW_DIR, "adventureworks_sales_customers.csv"))
        st.dataframe(df_cust, use_container_width=True)

# =================================================================================================
# View 5: Predictive Account Valuation
# =================================================================================================
elif section == "Predictive Account Valuation":
    st.markdown("#### Predictive Account Valuation Pipeline (LTV)")
    st.caption("Scikit-Learn Ridge Regression model calculating commercial Lifetime Value (LTV) scores based on order volume and past spend.")

    from app.services.baseline_analytics import SalesBaselineAnalyticsEngine

    if st.button("Run Valuation Pipeline Inference", type="primary", key="valuation_run_btn"):
        fit = SalesBaselineAnalyticsEngine.train_baseline_account_valuation_model()
        st.markdown(f"**Model Architecture:** `{fit['model_type']}` | **R² Fit Score:** `{fit['r2_fit_score']}`")
        st.dataframe(pd.DataFrame(fit["records"]), use_container_width=True)
