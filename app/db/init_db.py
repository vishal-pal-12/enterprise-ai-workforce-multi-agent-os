from app.db.session import engine, Base
from app.db.models import (
    GovernmentDataSource, DatasetIngestionRun, BusinessOpportunity,
    AgentRun, AgentExecutionEvent, ToolExecutionLog, OutreachMessage, ApprovalRequest
)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")

if __name__ == "__main__":
    init_db()
