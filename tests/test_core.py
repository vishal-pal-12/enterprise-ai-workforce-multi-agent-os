import pytest
import json
import os
import pandas as pd
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.db.models import GovernmentDataSource, BusinessOpportunity, OutreachMessage, ApprovalRequest
from app.services.data_pipeline import DataPipelineService
from app.services.email_service import EmailService
from app.agent.tools.sales_tools import (
    inspect_available_datasets,
    load_government_dataset,
    inspect_dataset_schema,
    validate_dataset,
    filter_enterprises,
    aggregate_enterprises_by_region,
    analyse_export_statistics,
    compare_regions,
    calculate_opportunity_score,
    save_business_opportunity,
    retrieve_saved_opportunities,
    prepare_outreach_message
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_db()
    DataPipelineService.sync_manifest_to_db()

def test_dataset_loading_and_pipeline():
    report = DataPipelineService.inspect_and_clean_dataset("udyam_msme")
    assert report["dataset_id"] == "udyam_msme"
    assert report["processed_records"] > 0
    assert "registered_units" in report["columns"]
    
    df = DataPipelineService.get_processed_dataframe("udyam_msme")
    assert not df.empty
    assert "state" in df.columns

def test_tool_inspect_available_datasets():
    res = json.loads(inspect_available_datasets.invoke({}))
    assert res["status"] == "SUCCESS"
    assert len(res["available_datasets"]) >= 2
    ids = [d["dataset_id"] for d in res["available_datasets"]]
    assert "udyam_msme" in ids
    assert "commodity_export" in ids

def test_tool_filter_enterprises():
    res = json.loads(filter_enterprises.invoke({"state": "Maharashtra"}))
    assert res["status"] == "SUCCESS"
    assert res["matches_count"] > 0
    for rec in res["records"]:
        assert rec["state"] == "Maharashtra"

def test_tool_aggregate_enterprises_by_region():
    res = json.loads(aggregate_enterprises_by_region.invoke({"group_by": "state"}))
    assert res["status"] == "SUCCESS"
    ranking = res["ranking"]
    assert len(ranking) > 0
    assert "total_registered_units" in ranking[0]
    # Check descending order
    assert ranking[0]["total_registered_units"] >= ranking[-1]["total_registered_units"]

def test_tool_analyse_export_statistics():
    res = json.loads(analyse_export_statistics.invoke({"sector": "Manufacturing"}))
    assert res["status"] == "SUCCESS"
    assert res["total_export_value_usd_million"] > 0
    assert len(res["commodities_ranked"]) > 0

def test_tool_calculate_opportunity_score():
    res = json.loads(calculate_opportunity_score.invoke({"state": "Maharashtra", "sector": "Engineering Goods"}))
    assert res["status"] == "SUCCESS"
    score = res["opportunity_score"]
    assert 0 <= score <= 100
    assert "Heuristic Prioritization Score" in res["explanation"]
    assert "not represent statistically verified probability" in res["explanation"]

def test_tool_save_and_retrieve_business_opportunity():
    save_res = json.loads(save_business_opportunity.invoke({
        "title": "Industrial Expansion Pune",
        "region": "Maharashtra",
        "sector": "Manufacturing",
        "evidence_summary": "High concentration of Small and Medium MSME units in Pune district.",
        "score": 85.5,
        "score_explanation": "Test explanation based on empirical registrations."
    }))
    assert save_res["status"] == "SUCCESS"
    opp_id = save_res["opportunity_id"]

    retrieve_res = json.loads(retrieve_saved_opportunities.invoke({}))
    assert retrieve_res["status"] == "SUCCESS"
    matching = [o for o in retrieve_res["opportunities"] if o["id"] == opp_id]
    assert len(matching) == 1
    assert matching[0]["region"] == "Maharashtra"

def test_outreach_approval_and_duplicate_protection():
    db = SessionLocal()
    try:
        # Create opportunity
        opp = BusinessOpportunity(
            title="Tamil Nadu Electronics",
            region="Tamil Nadu",
            sector="Electronics",
            evidence_summary="Chennai electronics ecosystem.",
            source_dataset="udyam_msme",
            source_reporting_period="2023-2024",
            opportunity_score=80.0
        )
        db.add(opp)
        db.commit()
        db.refresh(opp)

        # 1. Draft outreach
        draft_str = prepare_outreach_message.invoke({
            "opportunity_id": opp.id,
            "recipient_email": "procurement@chennai-tech.in",
            "recipient_name": "Procurement Lead",
            "sender_company_pitch": "Automated supply chain platform"
        })
        draft_res = json.loads(draft_str)
        msg_id = draft_res["message_id"]

        # 2. Try sending WITHOUT approval -> MUST FAIL (Security Violation)
        unapproved_send = EmailService.dispatch_message(db, msg_id)
        assert unapproved_send["status"] == "ERROR"
        assert "NOT received human-in-the-loop approval" in unapproved_send["error"]

        # 3. Approve
        approval_res = EmailService.approve_message(db, msg_id, approver="ComplianceOfficer", notes="Approved")
        assert approval_res["status"] == "SUCCESS"

        # 4. Dispatch with mock provider
        send_res = EmailService.dispatch_message(db, msg_id)
        assert send_res["status"] == "SUCCESS"
        assert send_res["provider_message_id"] is not None

        # 5. Try sending AGAIN -> MUST FAIL (Duplicate-Send Protection)
        dup_send = EmailService.dispatch_message(db, msg_id)
        assert dup_send["status"] == "ERROR"
        assert "Duplicate-Send Protection" in dup_send["error"]
    finally:
        db.close()
