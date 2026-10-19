from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from app.agent.sales_agent import SalesIntelligenceAgent
from app.db.session import SessionLocal
from app.db.models import AgentRun

def test_sales_agent_missing_llm_reporting():
    # If no LLM keys are configured, agent should cleanly record failure with informative guidance, NOT hallucinate
    from app.config import settings
    orig_google = settings.GOOGLE_API_KEY
    orig_openai = settings.OPENAI_API_KEY
    try:
        settings.GOOGLE_API_KEY = ""
        settings.OPENAI_API_KEY = ""
        agent = SalesIntelligenceAgent()
        result = agent.execute("Analyze top MSME regions")
        assert result["status"] == "FAILED"
        assert "LLM Provider is not configured" in result["error"]
    finally:
        settings.GOOGLE_API_KEY = orig_google
        settings.OPENAI_API_KEY = orig_openai

def test_sales_agent_mocked_llm_tool_calling(monkeypatch):
    """
    Verifies the bounded execution loop:
    Step 1: Mock LLM requests tool aggregate_enterprises_by_region
    Step 2: Mock LLM receives tool output and returns final synthesis response
    """
    mock_llm = MagicMock()
    tool_call_payload = {
        "name": "aggregate_enterprises_by_region",
        "args": {"group_by": "state"},
        "id": "call_abc123"
    }
    
    # First invoke returns tool call
    step_1_msg = AIMessage(
        content="I will aggregate registered units by state using aggregate_enterprises_by_region.",
        tool_calls=[tool_call_payload]
    )
    # Second invoke returns final grounded response
    step_2_msg = AIMessage(
        content="Based on verified Udyam records for 2023-2024, Maharashtra and Gujarat lead in registered enterprise counts."
    )

    mock_llm_with_tools = MagicMock()
    mock_llm_with_tools.invoke.side_effect = [step_1_msg, step_2_msg]
    mock_llm.bind_tools.return_value = mock_llm_with_tools

    monkeypatch.setattr("app.agent.sales_agent.get_configured_llm", lambda: mock_llm)

    agent = SalesIntelligenceAgent()
    res = agent.execute("Identify leading enterprise regions in India", max_steps=4)

    assert res["status"] == "COMPLETED"
    assert res["executed_tools_count"] == 1
    assert "Maharashtra" in res["final_response"]
    
    # Check trace events recorded in database
    event_types = [e["event_type"] for e in res["events"]]
    assert "INIT" in event_types
    assert "TOOL_CALL" in event_types
    assert "TOOL_RESULT" in event_types
    assert "FINISH" in event_types
