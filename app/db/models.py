import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Float, Integer, Boolean, DateTime, JSON, ForeignKey
)
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc)

class GovernmentDataSource(Base):
    __tablename__ = "government_data_sources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dataset_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    official_url = Column(String(500), nullable=False)
    catalog_url = Column(String(500), nullable=True)
    local_file = Column(String(255), nullable=False)
    reporting_period = Column(String(100), nullable=False)
    granularity = Column(String(100), nullable=False)
    units = Column(String(100), nullable=True)
    is_synthetic_seed = Column(Boolean, default=False)
    license = Column(String(150), default="GODL")
    limitations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    ingestion_runs = relationship("DatasetIngestionRun", back_populates="source")

class DatasetIngestionRun(Base):
    __tablename__ = "dataset_ingestion_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dataset_id = Column(String(100), ForeignKey("government_data_sources.dataset_id"), nullable=False)
    raw_file_path = Column(String(500), nullable=False)
    processed_file_path = Column(String(500), nullable=True)
    row_count = Column(Integer, default=0)
    columns_detected = Column(JSON, nullable=True)
    missing_values_count = Column(JSON, nullable=True)
    validation_status = Column(String(50), default="PENDING")
    quality_warnings = Column(JSON, nullable=True)
    executed_at = Column(DateTime, default=utc_now)

    source = relationship("GovernmentDataSource", back_populates="ingestion_runs")

class BusinessOpportunity(Base):
    __tablename__ = "business_opportunities"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    region = Column(String(100), index=True, nullable=False)
    sector = Column(String(100), index=True, nullable=False)
    evidence_summary = Column(Text, nullable=False)
    source_dataset = Column(String(100), nullable=False)
    source_reporting_period = Column(String(100), nullable=False)
    opportunity_score = Column(Float, nullable=True)
    score_explanation = Column(Text, nullable=True)
    status = Column(String(50), default="DISCOVERED") # DISCOVERED, SAVED, OUTREACH_PENDING, CONTACTED, CLOSED
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    messages = relationship("OutreachMessage", back_populates="opportunity")

class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_objective = Column(Text, nullable=False)
    agent_name = Column(String(100), default="SalesIntelligenceAgent")
    status = Column(String(50), default="RUNNING") # RUNNING, COMPLETED, FAILED
    plan = Column(JSON, nullable=True)
    final_response = Column(Text, nullable=True)
    structured_findings = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    completed_at = Column(DateTime, nullable=True)

    events = relationship("AgentExecutionEvent", back_populates="run", cascade="all, delete-orphan")
    tool_logs = relationship("ToolExecutionLog", back_populates="run", cascade="all, delete-orphan")

class AgentExecutionEvent(Base):
    __tablename__ = "agent_execution_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    run_id = Column(String(36), ForeignKey("agent_runs.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    event_type = Column(String(50), nullable=False) # PLAN, TOOL_CALL, TOOL_RESULT, EVALUATION, ERROR, FINISH
    description = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=utc_now)

    run = relationship("AgentRun", back_populates="events")

class ToolExecutionLog(Base):
    __tablename__ = "tool_execution_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    run_id = Column(String(36), ForeignKey("agent_runs.id"), nullable=True)
    tool_name = Column(String(100), index=True, nullable=False)
    arguments = Column(JSON, nullable=True)
    result_summary = Column(Text, nullable=True)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    execution_time_ms = Column(Float, default=0.0)
    executed_at = Column(DateTime, default=utc_now)

    run = relationship("AgentRun", back_populates="tool_logs")

class OutreachMessage(Base):
    __tablename__ = "outreach_messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    opportunity_id = Column(String(36), ForeignKey("business_opportunities.id"), nullable=True)
    recipient_email = Column(String(255), nullable=False)
    recipient_name = Column(String(255), nullable=False)
    subject = Column(String(300), nullable=False)
    body_content = Column(Text, nullable=False)
    status = Column(String(50), default="DRAFT") # DRAFT, APPROVED, SENT, REJECTED, FAILED
    provider_message_id = Column(String(255), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    opportunity = relationship("BusinessOpportunity", back_populates="messages")
    approvals = relationship("ApprovalRequest", back_populates="message")

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    message_id = Column(String(36), ForeignKey("outreach_messages.id"), nullable=False)
    action_type = Column(String(100), default="SEND_OUTREACH_EMAIL")
    approver = Column(String(100), default="HumanInTheLoop_User")
    is_approved = Column(Boolean, default=False)
    approval_notes = Column(Text, nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    message = relationship("OutreachMessage", back_populates="approvals")
