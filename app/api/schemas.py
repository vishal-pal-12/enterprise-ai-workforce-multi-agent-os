from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AgentRunRequest(BaseModel):
    objective: str = Field(..., description="Business task or intelligence objective in natural language")
    max_steps: int = Field(8, description="Maximum bounded steps for the agent execution loop")

class AgentRunResponse(BaseModel):
    run_id: str
    status: str
    objective: str
    final_response: Optional[str] = None
    executed_tools_count: int
    events: List[Dict[str, Any]]

class IngestDatasetRequest(BaseModel):
    dataset_id: str = Field(..., description="Dataset identifier, e.g., 'udyam_msme' or 'commodity_export'")

class OpportunityCreateRequest(BaseModel):
    title: str
    region: str
    sector: str
    evidence_summary: str
    score: Optional[float] = None
    score_explanation: Optional[str] = None

class OpportunityResponse(BaseModel):
    id: str
    title: str
    region: str
    sector: str
    evidence_summary: str
    source_dataset: str
    source_reporting_period: str
    opportunity_score: Optional[float] = None
    score_explanation: Optional[str] = None
    status: str

class OutreachPrepareRequest(BaseModel):
    opportunity_id: str
    recipient_email: str
    recipient_name: str
    sender_company_pitch: str

class OutreachApproveRequest(BaseModel):
    approver: str = "HumanManager"
    notes: Optional[str] = "Approved after review."
