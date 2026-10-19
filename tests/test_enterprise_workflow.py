import pytest
import json
from app.agent.tools.sales_tools import (
    query_adventureworks_customers,
    evaluate_account_valuation_ml,
    analyze_incoming_customer_reply,
    execute_autonomous_sales_action
)

def test_query_adventureworks_customers():
    res_str = query_adventureworks_customers.invoke({"region": "Maharashtra"})
    res = json.loads(res_str)
    assert res["status"] == "SUCCESS"
    assert res["matches_count"] > 0
    for c in res["customers"]:
        assert c["region"] == "Maharashtra"
        assert "annual_revenue" in c

def test_evaluate_account_valuation_ml():
    res_str = evaluate_account_valuation_ml.invoke({})
    res = json.loads(res_str)
    assert res["status"] == "SUCCESS"
    assert "Ridge" in res["baseline_model"]
    assert res["r2_fit_score"] > 0.85
    assert len(res["evaluated_accounts"]) > 0

def test_analyze_incoming_customer_reply_interested():
    reply = "Hi Sales Team, we reviewed your proposal and would love to schedule a demo call this Thursday."
    res_str = analyze_incoming_customer_reply.invoke({
        "customer_email": "kavita.patel@westernprecision.in",
        "reply_text": reply
    })
    res = json.loads(res_str)
    assert res["status"] == "SUCCESS"
    assert res["detected_intent"] == "INTERESTED_IN_DEMO"
    assert res["sentiment"] == "POSITIVE"
    assert res["autonomous_recommended_action"] == "SCHEDULE_DISCOVERY_CALL"

def test_analyze_incoming_customer_reply_pricing():
    reply = "Could you please share the pricing breakdown and cost for multi-site deployment?"
    res_str = analyze_incoming_customer_reply.invoke({
        "customer_email": "rajesh.sharma@apex-mfg.in",
        "reply_text": reply
    })
    res = json.loads(res_str)
    assert res["status"] == "SUCCESS"
    assert res["detected_intent"] == "PRICING_INQUIRY"
    assert res["autonomous_recommended_action"] == "DISPATCH_TIERED_QUOTE"

def test_execute_autonomous_sales_action():
    res_str = execute_autonomous_sales_action.invoke({
        "customer_email": "kavita.patel@westernprecision.in",
        "action_type": "SCHEDULE_DISCOVERY_CALL",
        "action_summary": "Introductory discovery briefing booked for Thursday 2 PM."
    })
    res = json.loads(res_str)
    assert res["status"] == "SUCCESS"
    assert res["execution_mode"] == "AUTONOMOUS_BUSINESS_ACTION"

