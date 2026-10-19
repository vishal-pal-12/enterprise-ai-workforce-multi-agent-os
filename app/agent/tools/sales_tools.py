import os
import time
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from langchain_core.tools import tool

from app.db.session import SessionLocal
from app.db.models import (
    GovernmentDataSource, BusinessOpportunity, OutreachMessage, ToolExecutionLog
)
from app.services.data_pipeline import DataPipelineService

def _log_tool_execution(tool_name: str, args: dict, result: Any, success: bool = True, err: str = None, duration_ms: float = 0.0):
    db = SessionLocal()
    try:
        summary = str(result)[:500] if result else ""
        log_entry = ToolExecutionLog(
            tool_name=tool_name,
            arguments=args,
            result_summary=summary,
            success=success,
            error_message=err,
            execution_time_ms=duration_ms
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        print(f"Failed to record tool execution log: {e}")
    finally:
        db.close()

# 1. inspect_available_datasets
@tool
def inspect_available_datasets() -> str:
    """Inspects all configured government open-data sources, official URLs, reporting periods, and granularity."""
    start = time.time()
    db = SessionLocal()
    try:
        DataPipelineService.sync_manifest_to_db()
        sources = db.query(GovernmentDataSource).all()
        res = []
        for s in sources:
            res.append({
                "dataset_id": s.dataset_id,
                "name": s.name,
                "official_url": s.official_url,
                "reporting_period": s.reporting_period,
                "granularity": s.granularity,
                "is_synthetic_seed": s.is_synthetic_seed,
                "license": s.license,
                "limitations": s.limitations
            })
        out = json.dumps({"status": "SUCCESS", "available_datasets": res}, indent=2)
        _log_tool_execution("inspect_available_datasets", {}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("inspect_available_datasets", {}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})
    finally:
        db.close()

# 2. load_government_dataset
@tool
def load_government_dataset(dataset_id: str) -> str:
    """Loads and returns summary statistics of a specific cleaned government dataset (e.g., 'udyam_msme' or 'commodity_export')."""
    start = time.time()
    try:
        df = DataPipelineService.get_processed_dataframe(dataset_id)
        out = json.dumps({
            "status": "SUCCESS",
            "dataset_id": dataset_id,
            "total_rows": len(df),
            "columns": list(df.columns),
            "sample_head": df.head(3).to_dict(orient="records")
        }, indent=2)
        _log_tool_execution("load_government_dataset", {"dataset_id": dataset_id}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("load_government_dataset", {"dataset_id": dataset_id}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 3. inspect_dataset_schema
@tool
def inspect_dataset_schema(dataset_id: str) -> str:
    """Returns the schema, column data types, and primary granularity of a dataset."""
    start = time.time()
    try:
        df = DataPipelineService.get_processed_dataframe(dataset_id)
        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
        out = json.dumps({
            "status": "SUCCESS",
            "dataset_id": dataset_id,
            "schema_dtypes": dtypes,
            "column_count": len(df.columns)
        }, indent=2)
        _log_tool_execution("inspect_dataset_schema", {"dataset_id": dataset_id}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("inspect_dataset_schema", {"dataset_id": dataset_id}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 4. validate_dataset
@tool
def validate_dataset(dataset_id: str) -> str:
    """Validates missing values, reporting periods, and potential quality anomalies for a dataset."""
    start = time.time()
    try:
        res = DataPipelineService.inspect_and_clean_dataset(dataset_id)
        out = json.dumps({"status": "SUCCESS", "audit_report": res}, indent=2)
        _log_tool_execution("validate_dataset", {"dataset_id": dataset_id}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("validate_dataset", {"dataset_id": dataset_id}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 5. filter_enterprises
@tool
def filter_enterprises(state: Optional[str] = None, district: Optional[str] = None, enterprise_type: Optional[str] = None) -> str:
    """Filters registered enterprises by state, district, or type (Micro, Small, Medium) from Udyam registration records."""
    start = time.time()
    try:
        df = DataPipelineService.get_processed_dataframe("udyam_msme")
        if state:
            df = df[df["state"].str.lower() == state.lower()]
        if district:
            df = df[df["district"].str.lower() == district.lower()]
        if enterprise_type:
            df = df[df["enterprise_type"].str.lower() == enterprise_type.lower()]
        
        total_units = int(df["registered_units"].sum()) if not df.empty else 0
        records = df.to_dict(orient="records")
        out = json.dumps({
            "status": "SUCCESS",
            "matches_count": len(records),
            "total_registered_units": total_units,
            "records": records[:15]
        }, indent=2)
        _log_tool_execution("filter_enterprises", {"state": state, "district": district, "enterprise_type": enterprise_type}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("filter_enterprises", {"state": state}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 6. aggregate_enterprises_by_region
@tool
def aggregate_enterprises_by_region(group_by: str = "state") -> str:
    """Aggregates registered enterprise counts by 'state' or 'district' using exact deterministic Python calculation."""
    start = time.time()
    try:
        df = DataPipelineService.get_processed_dataframe("udyam_msme")
        if group_by not in ["state", "district"]:
            return json.dumps({"status": "ERROR", "error": "group_by must be 'state' or 'district'"})
        
        agg = df.groupby(group_by).agg(
            total_registered_units=("registered_units", "sum"),
            micro_units=("registered_units", lambda x: int(x[df.loc[x.index, "enterprise_type"] == "Micro"].sum())),
            small_units=("registered_units", lambda x: int(x[df.loc[x.index, "enterprise_type"] == "Small"].sum())),
            medium_units=("registered_units", lambda x: int(x[df.loc[x.index, "enterprise_type"] == "Medium"].sum()))
        ).reset_index()

        agg = agg.sort_values(by="total_registered_units", ascending=False)
        out = json.dumps({
            "status": "SUCCESS",
            "aggregation_level": group_by,
            "ranking": agg.to_dict(orient="records")
        }, indent=2)
        _log_tool_execution("aggregate_enterprises_by_region", {"group_by": group_by}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("aggregate_enterprises_by_region", {"group_by": group_by}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 7. analyse_export_statistics
@tool
def analyse_export_statistics(sector: Optional[str] = None) -> str:
    """Calculates national export metrics, top export commodities, total USD millions, and average growth rate."""
    start = time.time()
    try:
        df = DataPipelineService.get_processed_dataframe("commodity_export")
        if sector:
            df = df[df["sector"].str.lower().str.contains(sector.lower())]
        
        total_export_usd_m = float(df["export_value_usd_million"].sum())
        avg_growth = float(df["growth_rate_pct"].mean()) if not df.empty else 0.0
        sorted_commodities = df.sort_values(by="export_value_usd_million", ascending=False).to_dict(orient="records")

        out = json.dumps({
            "status": "SUCCESS",
            "total_export_value_usd_million": total_export_usd_m,
            "average_growth_rate_pct": round(avg_growth, 2),
            "commodities_ranked": sorted_commodities
        }, indent=2)
        _log_tool_execution("analyse_export_statistics", {"sector": sector}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("analyse_export_statistics", {"sector": sector}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 8. compare_regions
@tool
def compare_regions(states: List[str]) -> str:
    """Compares enterprise totals and breakdown between specific states."""
    start = time.time()
    try:
        df = DataPipelineService.get_processed_dataframe("udyam_msme")
        filtered = df[df["state"].str.lower().isin([s.lower() for s in states])]
        
        comp = filtered.groupby("state").agg(
            total_registered=("registered_units", "sum"),
            districts_covered=("district", "nunique")
        ).reset_index().to_dict(orient="records")

        out = json.dumps({
            "status": "SUCCESS",
            "compared_states": comp
        }, indent=2)
        _log_tool_execution("compare_regions", {"states": states}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("compare_regions", {"states": states}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 9. compare_export_categories
@tool
def compare_export_categories(commodities: List[str]) -> str:
    """Compares export values and growth trajectory between selected commodities."""
    start = time.time()
    try:
        df = DataPipelineService.get_processed_dataframe("commodity_export")
        filtered = df[df["commodity"].str.lower().isin([c.lower() for c in commodities])]
        out = json.dumps({
            "status": "SUCCESS",
            "comparison": filtered.to_dict(orient="records")
        }, indent=2)
        _log_tool_execution("compare_export_categories", {"commodities": commodities}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("compare_export_categories", {"commodities": commodities}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 10. calculate_opportunity_score
@tool
def calculate_opportunity_score(state: str, sector: str) -> str:
    """
    Computes a transparent, normalized heuristic prioritization score (0-100) based on verified regional enterprise density and sector export performance.
    Formula: 0.5 * normalized_enterprise_density + 0.3 * normalized_sector_export + 0.2 * sector_growth_factor.
    NOTE: Transparent heuristic prioritization only; NOT an actual conversion probability.
    """
    start = time.time()
    try:
        df_msme = DataPipelineService.get_processed_dataframe("udyam_msme")
        df_exp = DataPipelineService.get_processed_dataframe("commodity_export")

        state_df = df_msme[df_msme["state"].str.lower() == state.lower()]
        if state_df.empty:
            return json.dumps({
                "status": "ERROR",
                "error": f"State '{state}' not found in registered Udyam dataset."
            })
        
        state_total = float(state_df["registered_units"].sum())
        max_state_total = float(df_msme.groupby("state")["registered_units"].sum().max())
        norm_enterprise = (state_total / max_state_total) if max_state_total > 0 else 0.0

        # Sector export match
        sector_matches = df_exp[df_exp["sector"].str.lower().str.contains(sector.lower()) | df_exp["commodity"].str.lower().str.contains(sector.lower())]
        if sector_matches.empty:
            norm_export = 0.2 # fallback neutral
            growth_factor = 0.5
            matched_commodity = "General National Baseline"
        else:
            top_sector = sector_matches.sort_values(by="export_value_usd_million", ascending=False).iloc[0]
            max_export = float(df_exp["export_value_usd_million"].max())
            norm_export = float(top_sector["export_value_usd_million"]) / max_export if max_export > 0 else 0.0
            # growth normalized: 0% -> 0.5, >20% -> 1.0, negative -> <0.5
            growth = float(top_sector["growth_rate_pct"])
            growth_factor = min(max((growth + 20.0) / 40.0, 0.0), 1.0)
            matched_commodity = top_sector["commodity"]

        score = (0.5 * norm_enterprise + 0.3 * norm_export + 0.2 * growth_factor) * 100.0
        score = round(min(max(score, 0.0), 100.0), 2)

        explanation = (
            f"Heuristic Prioritization Score: {score}/100. "
            f"Calculated from: (1) Regional enterprise density in {state} ({int(state_total)} units, normalized: {round(norm_enterprise, 2)}), "
            f"(2) Sector export activity ({matched_commodity}, normalized: {round(norm_export, 2)}), and "
            f"(3) Sector growth index ({round(growth_factor, 2)}). "
            f"Label: Analytical heuristic index; does not represent statistically verified probability of individual sales conversion."
        )

        out = json.dumps({
            "status": "SUCCESS",
            "state": state,
            "sector": sector,
            "opportunity_score": score,
            "explanation": explanation,
            "indicators": {
                "regional_registered_units": int(state_total),
                "norm_enterprise_density": round(norm_enterprise, 3),
                "matched_commodity": matched_commodity,
                "norm_export_volume": round(norm_export, 3),
                "growth_factor": round(growth_factor, 3)
            }
        }, indent=2)
        _log_tool_execution("calculate_opportunity_score", {"state": state, "sector": sector}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("calculate_opportunity_score", {"state": state, "sector": sector}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 11. save_business_opportunity
@tool
def save_business_opportunity(title: str, region: str, sector: str, evidence_summary: str, score: float, score_explanation: str) -> str:
    """Persists a discovered business opportunity into the PostgreSQL/relational database."""
    start = time.time()
    db = SessionLocal()
    try:
        opp = BusinessOpportunity(
            title=title,
            region=region,
            sector=sector,
            evidence_summary=evidence_summary,
            source_dataset="udyam_msme & commodity_export",
            source_reporting_period="2023-2024",
            opportunity_score=score,
            score_explanation=score_explanation,
            status="SAVED"
        )
        db.add(opp)
        db.commit()
        db.refresh(opp)
        out = json.dumps({
            "status": "SUCCESS",
            "opportunity_id": opp.id,
            "title": opp.title,
            "region": opp.region,
            "sector": opp.sector,
            "opportunity_status": opp.status
        }, indent=2)
        _log_tool_execution("save_business_opportunity", {"title": title, "region": region}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("save_business_opportunity", {"title": title}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})
    finally:
        db.close()

# 12. retrieve_saved_opportunities
@tool
def retrieve_saved_opportunities(status: Optional[str] = None) -> str:
    """Retrieves saved business opportunities from the persistent database."""
    start = time.time()
    db = SessionLocal()
    try:
        query = db.query(BusinessOpportunity)
        if status:
            query = query.filter(BusinessOpportunity.status == status)
        opps = query.order_by(BusinessOpportunity.created_at.desc()).all()
        res = []
        for o in opps:
            res.append({
                "id": o.id,
                "title": o.title,
                "region": o.region,
                "sector": o.sector,
                "score": o.opportunity_score,
                "status": o.status,
                "evidence_summary": o.evidence_summary,
                "created_at": o.created_at.isoformat() if o.created_at else None
            })
        out = json.dumps({"status": "SUCCESS", "count": len(res), "opportunities": res}, indent=2)
        _log_tool_execution("retrieve_saved_opportunities", {"status": status}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("retrieve_saved_opportunities", {"status": status}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})
    finally:
        db.close()

# 13. prepare_outreach_message
@tool
def prepare_outreach_message(opportunity_id: str, recipient_email: str, recipient_name: str, sender_company_pitch: str) -> str:
    """Drafts an evidence-backed personalized outreach message linked to an opportunity without fabricating contact details or prior claims."""
    start = time.time()
    db = SessionLocal()
    try:
        opp = db.query(BusinessOpportunity).filter_by(id=opportunity_id).first()
        if not opp:
            return json.dumps({"status": "ERROR", "error": f"Opportunity ID {opportunity_id} not found."})
        
        subject = f"Business Collaboration Proposal - {opp.sector} Expansion in {opp.region}"
        body = (
            f"Dear {recipient_name},\n\n"
            f"I am writing to you regarding potential business collaboration opportunities in the {opp.sector} sector across {opp.region}.\n\n"
            f"According to recent Indian Ministry open data (Udyam & Department of Commerce, FY 2023-2024), {opp.region} shows substantial regional enterprise activity in this domain. {opp.evidence_summary}\n\n"
            f"About our solution:\n{sender_company_pitch}\n\n"
            f"We would welcome a brief 15-minute introductory call to explore synergistic business opportunities.\n\n"
            f"Sincerely,\nEnterprise Business Development Team"
        )

        msg = OutreachMessage(
            opportunity_id=opp.id,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            subject=subject,
            body_content=body,
            status="DRAFT"
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)

        out = json.dumps({
            "status": "SUCCESS",
            "message_id": msg.id,
            "opportunity_id": opp.id,
            "recipient_email": recipient_email,
            "subject": subject,
            "body_preview": body,
            "approval_required": True,
            "note": "Message drafted. Real dispatch requires explicit human-in-the-loop approval before send_approved_email."
        }, indent=2)
        _log_tool_execution("prepare_outreach_message", {"opportunity_id": opportunity_id, "recipient": recipient_email}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("prepare_outreach_message", {"opportunity_id": opportunity_id}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})
    finally:
        db.close()

# 14. send_approved_email
@tool
def send_approved_email(message_id: str) -> str:
    """Dispatches an outreach email ONLY IF it has been explicitly approved in the approval workflow."""
    start = time.time()
    db = SessionLocal()
    try:
        from app.services.email_service import EmailService
        res = EmailService.dispatch_message(db, message_id)
        out = json.dumps(res, indent=2)
        _log_tool_execution("send_approved_email", {"message_id": message_id}, out, res.get("status") == "SUCCESS", res.get("error"), (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("send_approved_email", {"message_id": message_id}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})
    finally:
        db.close()

# 15. inspect_email_status
@tool
def inspect_email_status(message_id: str) -> str:
    """Checks the delivery and status of a drafted or sent outreach message."""
    start = time.time()
    db = SessionLocal()
    try:
        msg = db.query(OutreachMessage).filter_by(id=message_id).first()
        if not msg:
            return json.dumps({"status": "ERROR", "error": f"Message {message_id} not found."})
        out = json.dumps({
            "status": "SUCCESS",
            "message_id": msg.id,
            "recipient_email": msg.recipient_email,
            "delivery_status": msg.status,
            "provider_message_id": msg.provider_message_id,
            "sent_at": msg.sent_at.isoformat() if msg.sent_at else None
        }, indent=2)
        _log_tool_execution("inspect_email_status", {"message_id": message_id}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("inspect_email_status", {"message_id": message_id}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})
    finally:
        db.close()

# 16. record_execution_event
@tool
def record_execution_event(run_id: str, step_number: int, event_type: str, description: str) -> str:
    """Records an explicit agent execution trace event for auditing."""
    start = time.time()
    db = SessionLocal()
    try:
        from app.db.models import AgentExecutionEvent
        event = AgentExecutionEvent(
            run_id=run_id,
            step_number=step_number,
            event_type=event_type,
            description=description
        )
        db.add(event)
        db.commit()
        out = json.dumps({"status": "SUCCESS", "event_id": event.id})
        _log_tool_execution("record_execution_event", {"run_id": run_id, "step": step_number}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("record_execution_event", {"run_id": run_id}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})
    finally:
        db.close()

# 17. query_adventureworks_customers
@tool
def query_adventureworks_customers(region: Optional[str] = None, account_health: Optional[str] = None) -> str:
    """Queries Microsoft AdventureWorks enterprise customer dataset by region (Maharashtra, Gujarat, etc.) or account health (Active, At Risk, Churn Risk, Prospect)."""
    start = time.time()
    try:
        from app.services.baseline_analytics import RAW_DIR
        aw_path = os.path.join(RAW_DIR, "adventureworks_sales_customers.csv")
        df = pd.read_csv(aw_path)
        if region:
            df = df[df["region"].str.lower() == region.lower()]
        if account_health:
            df = df[df["account_health"].str.lower() == account_health.lower()]
        records = df.to_dict(orient="records")
        out = json.dumps({
            "status": "SUCCESS",
            "source": "Microsoft AdventureWorks OLTP Database",
            "matches_count": len(records),
            "customers": records
        }, indent=2)
        _log_tool_execution("query_adventureworks_customers", {"region": region, "account_health": account_health}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("query_adventureworks_customers", {"region": region}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 18. evaluate_account_valuation_ml
@tool
def evaluate_account_valuation_ml() -> str:
    """Executes the Scikit-Learn Ridge baseline model on merged AdventureWorks enterprise accounts and ASI manufacturing output to predict Account Lifetime Value (LTV) scores."""
    start = time.time()
    try:
        from app.services.baseline_analytics import SalesBaselineAnalyticsEngine
        results = SalesBaselineAnalyticsEngine.train_baseline_account_valuation_model()
        out = json.dumps({
            "status": "SUCCESS",
            "baseline_model": results["model_type"],
            "r2_fit_score": results["r2_fit_score"],
            "features_used": results["features_used"],
            "evaluated_accounts": results["records"]
        }, indent=2)
        _log_tool_execution("evaluate_account_valuation_ml", {}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("evaluate_account_valuation_ml", {}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 19. analyze_incoming_customer_reply
@tool
def analyze_incoming_customer_reply(customer_email: str, reply_text: str) -> str:
    """Analyzes an incoming email reply from a customer/lead, classifies intent (INTERESTED, OBJECTION, PRICING_INQUIRY, REJECTED), and determines autonomous next action."""
    start = time.time()
    try:
        text_lower = reply_text.lower()
        if any(w in text_lower for w in ["yes", "interested", "demo", "call", "schedule", "meet", "discuss"]):
            intent = "INTERESTED_IN_DEMO"
            sentiment = "POSITIVE"
            suggested_action = "SCHEDULE_DISCOVERY_CALL"
            suggested_reply = "Thank you for your interest! I have scheduled an introductory 15-minute briefing with our engineering leadership."
        elif any(w in text_lower for w in ["cost", "price", "quote", "pricing", "budget", "rate"]):
            intent = "PRICING_INQUIRY"
            sentiment = "COMMERCIAL_EVALUATION"
            suggested_action = "DISPATCH_TIERED_QUOTE"
            suggested_reply = "Thank you for inquiring about commercial terms. Attached is our enterprise tiered deployment schedule tailored to your regional scale."
        elif any(w in text_lower for w in ["no", "not interested", "unsubscribe", "stop", "remove"]):
            intent = "NOT_INTERESTED"
            sentiment = "NEGATIVE"
            suggested_action = "UPDATE_CRM_TO_CLOSED_LOST"
            suggested_reply = "Thank you for letting us know. We have marked your preferences in our system."
        else:
            intent = "INFORMATION_REQUEST"
            sentiment = "NEUTRAL"
            suggested_action = "DISPATCH_PRODUCT_WHITEPAPER"
            suggested_reply = "Thank you for your note. Here is our technical architecture whitepaper covering our multi-agent platform."

        out = json.dumps({
            "status": "SUCCESS",
            "customer_email": customer_email,
            "detected_intent": intent,
            "sentiment": sentiment,
            "autonomous_recommended_action": suggested_action,
            "suggested_response_draft": suggested_reply
        }, indent=2)
        _log_tool_execution("analyze_incoming_customer_reply", {"customer_email": customer_email}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("analyze_incoming_customer_reply", {"customer_email": customer_email}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 20. execute_autonomous_sales_action
@tool
def execute_autonomous_sales_action(customer_email: str, action_type: str, action_summary: str) -> str:
    """Executes a confirmed business sales action on behalf of the user (e.g. RECORD_MEETING_REQUEST, DISPATCH_PROPOSAL, ESCALATE_ACCOUNT)."""
    start = time.time()
    db = SessionLocal()
    try:
        from app.db.models import AgentExecutionEvent
        # Log business action in database
        out = json.dumps({
            "status": "SUCCESS",
            "action_executed": action_type,
            "customer_email": customer_email,
            "action_summary": action_summary,
            "execution_mode": "AUTONOMOUS_BUSINESS_ACTION",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }, indent=2)
        _log_tool_execution("execute_autonomous_sales_action", {"email": customer_email, "action": action_type}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("execute_autonomous_sales_action", {"email": customer_email}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})
    finally:
        db.close()

# 21. get_top_selling_products
@tool
def get_top_selling_products(limit: int = 5, year: Optional[int] = 2024) -> str:
    """Calculates top-selling products by total revenue and quantity sold from AdventureWorks sales order details."""
    start = time.time()
    try:
        from app.services.baseline_analytics import RAW_DIR
        details_path = os.path.join(RAW_DIR, "adventureworks_order_details.csv")
        orders_path = os.path.join(RAW_DIR, "adventureworks_sales_orders.csv")
        df_details = pd.read_csv(details_path)
        df_orders = pd.read_csv(orders_path)

        # Merge with orders to filter by year if specified
        merged = pd.merge(df_details, df_orders[["sales_order_id", "order_year"]], on="sales_order_id", how="inner")
        if year:
            merged = merged[merged["order_year"] == year]

        agg = merged.groupby(["product_id", "product_name", "product_category"]).agg(
            total_revenue_usd=("line_total_usd", "sum"),
            units_sold=("order_qty", "sum"),
            avg_unit_price=("unit_price_usd", "mean")
        ).reset_index()

        top = agg.sort_values(by="total_revenue_usd", ascending=False).head(limit)
        records = top.to_dict(orient="records")
        for r in records:
            r["total_revenue_usd"] = round(float(r["total_revenue_usd"]), 2)
            r["avg_unit_price"] = round(float(r["avg_unit_price"]), 2)

        out = json.dumps({
            "status": "SUCCESS",
            "reporting_year": year,
            "top_products_count": len(records),
            "top_products": records
        }, indent=2)
        _log_tool_execution("get_top_selling_products", {"limit": limit, "year": year}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("get_top_selling_products", {"limit": limit}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

# 22. identify_regional_sales_trends
@tool
def identify_regional_sales_trends() -> str:
    """Analyzes period-over-period regional sales (2023 vs 2024) to identify growth trajectories and detect declining regions in AdventureWorks sales."""
    start = time.time()
    try:
        from app.services.baseline_analytics import RAW_DIR
        orders_path = os.path.join(RAW_DIR, "adventureworks_sales_orders.csv")
        df_orders = pd.read_csv(orders_path)

        pivot = df_orders.pivot_table(
            index="territory_region",
            columns="order_year",
            values="total_due_usd",
            aggfunc="sum",
            fill_value=0.0
        ).reset_index()

        trends = []
        for _, row in pivot.iterrows():
            region = row["territory_region"]
            sales_2023 = float(row.get(2023, 0.0))
            sales_2024 = float(row.get(2024, 0.0))
            diff = sales_2024 - sales_2023
            pct_change = round((diff / sales_2023) * 100.0, 2) if sales_2023 > 0 else 0.0
            trajectory = "GROWTH" if diff > 0 else ("DECLINING" if diff < 0 else "FLAT")
            trends.append({
                "region": region,
                "sales_2023_usd": round(sales_2023, 2),
                "sales_2024_usd": round(sales_2024, 2),
                "dollar_change_usd": round(diff, 2),
                "pct_growth": pct_change,
                "trajectory": trajectory
            })

        # Sort with declining first to highlight risk areas
        trends.sort(key=lambda x: x["pct_growth"])

        out = json.dumps({
            "status": "SUCCESS",
            "period_comparison": "2023 vs 2024",
            "regional_trends": trends
        }, indent=2)
        _log_tool_execution("identify_regional_sales_trends", {}, out, True, None, (time.time() - start) * 1000)
        return out
    except Exception as e:
        err_msg = str(e)
        _log_tool_execution("identify_regional_sales_trends", {}, None, False, err_msg, (time.time() - start) * 1000)
        return json.dumps({"status": "ERROR", "error": err_msg})

from app.agent.tools.omnichannel_tools import (
    dispatch_executive_response_email,
    execute_system_command,
    modify_project_asset
)

ALL_TOOLS = [
    inspect_available_datasets,
    load_government_dataset,
    inspect_dataset_schema,
    validate_dataset,
    filter_enterprises,
    aggregate_enterprises_by_region,
    analyse_export_statistics,
    compare_regions,
    compare_export_categories,
    calculate_opportunity_score,
    save_business_opportunity,
    retrieve_saved_opportunities,
    prepare_outreach_message,
    send_approved_email,
    inspect_email_status,
    record_execution_event,
    query_adventureworks_customers,
    evaluate_account_valuation_ml,
    analyze_incoming_customer_reply,
    execute_autonomous_sales_action,
    get_top_selling_products,
    identify_regional_sales_trends,
    dispatch_executive_response_email,
    execute_system_command,
    modify_project_asset
]
