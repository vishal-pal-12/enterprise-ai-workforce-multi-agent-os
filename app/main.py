from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.db.init_db import init_db
from app.db.models import (
    GovernmentDataSource, DatasetIngestionRun, BusinessOpportunity,
    AgentRun, AgentExecutionEvent, OutreachMessage, ApprovalRequest
)
from app.services.data_pipeline import DataPipelineService
from app.services.email_service import EmailService
from app.agent.sales_agent import SalesIntelligenceAgent
from app.api.schemas import (
    AgentRunRequest, AgentRunResponse, IngestDatasetRequest,
    OpportunityCreateRequest, OpportunityResponse,
    OutreachPrepareRequest, OutreachApproveRequest
)

app = FastAPI(
    title="AI-Powered Enterprise Multi-Agent Operating System",
    description="Backend API powering the Sales Intelligence & Business Development Agent with genuine tool calling and government open-data integration.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    from app.db.init_db import init_db
    init_db()
    DataPipelineService.sync_manifest_to_db()

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "HEALTHY", "system": "Multi-Agent Enterprise OS", "active_agent": "SalesIntelligenceAgent"}

# Agent Execution Endpoints
@app.post("/agent/run", response_model=AgentRunResponse, tags=["Agent"])
def run_agent(req: AgentRunRequest):
    agent = SalesIntelligenceAgent()
    result = agent.execute(objective=req.objective, max_steps=req.max_steps)
    return result

@app.get("/agent/runs/{run_id}", tags=["Agent"])
def get_agent_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(AgentRun).filter_by(id=run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Agent run not found")
    events = db.query(AgentExecutionEvent).filter_by(run_id=run_id).order_by(AgentExecutionEvent.step_number.asc()).all()
    return {
        "run_id": run.id,
        "objective": run.user_objective,
        "status": run.status,
        "final_response": run.final_response,
        "created_at": run.created_at,
        "completed_at": run.completed_at,
        "events": [
            {
                "step": e.step_number,
                "event_type": e.event_type,
                "description": e.description,
                "metadata": e.metadata_json,
                "timestamp": e.timestamp
            }
            for e in events
        ]
    }

# Dataset Endpoints
@app.get("/datasets", tags=["Datasets"])
def list_datasets(db: Session = Depends(get_db)):
    sources = db.query(GovernmentDataSource).all()
    return sources

@app.post("/datasets/ingest", tags=["Datasets"])
def ingest_dataset(req: IngestDatasetRequest):
    try:
        report = DataPipelineService.inspect_and_clean_dataset(req.dataset_id)
        return {"status": "SUCCESS", "report": report}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/datasets/{dataset_id}/schema", tags=["Datasets"])
def get_dataset_schema(dataset_id: str):
    try:
        df = DataPipelineService.get_processed_dataframe(dataset_id)
        return {
            "dataset_id": dataset_id,
            "columns": list(df.columns),
            "dtypes": {c: str(d) for c, d in df.dtypes.items()},
            "row_count": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# Opportunity Management Endpoints
@app.post("/opportunities", response_model=OpportunityResponse, tags=["Opportunities"])
def create_opportunity(req: OpportunityCreateRequest, db: Session = Depends(get_db)):
    opp = BusinessOpportunity(
        title=req.title,
        region=req.region,
        sector=req.sector,
        evidence_summary=req.evidence_summary,
        source_dataset="udyam_msme & commodity_export",
        source_reporting_period="2023-2024",
        opportunity_score=req.score,
        score_explanation=req.score_explanation,
        status="SAVED"
    )
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return opp

@app.get("/opportunities", response_model=List[OpportunityResponse], tags=["Opportunities"])
def list_opportunities(db: Session = Depends(get_db)):
    return db.query(BusinessOpportunity).order_by(BusinessOpportunity.created_at.desc()).all()

@app.get("/opportunities/{opportunity_id}", response_model=OpportunityResponse, tags=["Opportunities"])
def get_opportunity(opportunity_id: str, db: Session = Depends(get_db)):
    opp = db.query(BusinessOpportunity).filter_by(id=opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp

# Outreach Workflow Endpoints
@app.post("/outreach/prepare", tags=["Outreach"])
def prepare_outreach(req: OutreachPrepareRequest, db: Session = Depends(get_db)):
    from app.agent.tools.sales_tools import prepare_outreach_message
    res_str = prepare_outreach_message.invoke({
        "opportunity_id": req.opportunity_id,
        "recipient_email": req.recipient_email,
        "recipient_name": req.recipient_name,
        "sender_company_pitch": req.sender_company_pitch
    })
    import json
    return json.loads(res_str)

@app.post("/outreach/{message_id}/approve", tags=["Outreach"])
def approve_outreach(message_id: str, req: OutreachApproveRequest, db: Session = Depends(get_db)):
    res = EmailService.approve_message(db, message_id, req.approver, req.notes)
    if res.get("status") == "ERROR":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res

@app.post("/outreach/{message_id}/send", tags=["Outreach"])
def send_outreach(message_id: str, db: Session = Depends(get_db)):
    res = EmailService.dispatch_message(db, message_id)
    if res.get("status") == "ERROR":
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res

@app.get("/outreach/{message_id}/status", tags=["Outreach"])
def get_outreach_status(message_id: str, db: Session = Depends(get_db)):
    msg = db.query(OutreachMessage).filter_by(id=message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return {
        "id": msg.id,
        "recipient_email": msg.recipient_email,
        "recipient_name": msg.recipient_name,
        "subject": msg.subject,
        "status": msg.status,
        "provider_message_id": msg.provider_message_id,
        "sent_at": msg.sent_at
    }

@app.get("/outreach", tags=["Outreach"])
def list_outreach_messages(db: Session = Depends(get_db)):
    msgs = db.query(OutreachMessage).order_by(OutreachMessage.created_at.desc()).all()
    return msgs
