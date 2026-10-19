import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["active_agent"] == "SalesIntelligenceAgent"

def test_datasets_endpoint():
    response = client.get("/datasets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def test_opportunity_flow_endpoints():
    # 1. Create opportunity
    create_payload = {
        "title": "FastAPI IT Sector Hub Bangalore",
        "region": "Karnataka",
        "sector": "Information Technology",
        "evidence_summary": "Extensive IT and MSME technology cluster in Bengaluru Urban.",
        "score": 92.4,
        "score_explanation": "Analytical calculation based on export volumes and registered density."
    }
    res = client.post("/opportunities", json=create_payload)
    assert res.status_code == 200
    opp = res.json()
    opp_id = opp["id"]
    assert opp["region"] == "Karnataka"

    # 2. Get opportunity
    get_res = client.get(f"/opportunities/{opp_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == create_payload["title"]

    # 3. Draft outreach
    draft_payload = {
        "opportunity_id": opp_id,
        "recipient_email": "cto@tech-enterprise.in",
        "recipient_name": "CTO",
        "sender_company_pitch": "Automated AI decision OS"
    }
    draft_res = client.post("/outreach/prepare", json=draft_payload)
    assert draft_res.status_code == 200
    msg_id = draft_res.json()["message_id"]

    # 4. Approve outreach
    approve_res = client.post(f"/outreach/{msg_id}/approve", json={"approver": "SeniorVP"})
    assert approve_res.status_code == 200
    assert approve_res.json()["status"] == "SUCCESS"

    # 5. Send outreach
    send_res = client.post(f"/outreach/{msg_id}/send")
    assert send_res.status_code == 200
    assert send_res.json()["status"] == "SUCCESS"
