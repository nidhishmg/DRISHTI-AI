from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .logging import logger
from ..schemas.models import TraceLog, TraceStatus, ProcessingStage
import os
import json

class AuditLogger:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/drushti")
        # Ensure we use asyncpg driver or compatible for async, but for simple logging sync might be okay or use separate connection.
        # Since this is "AuditLogger" it might be called from sync or async contexts. 
        # For simplicity in this phase, using sync engine for the logger as it might be used in background threads 
        # or we assume standard synchronous logging for reliability.
        # Actually requirements.txt has 'asyncpg' and 'sqlalchemy'. 
        # I'll stick to a synchronous engine for the audit logger for now to ensure it blocks/persists reliably 
        # without complex async context management in every call, OR make it purely async if the rest is async.
        # Given "QueueConsumer" and "IngestionWorker" likely async, let's make a clear interface. 
        # But wait, SQLAlchemy 2.0 supports sync style with async engine too? No.
        # Let's use psycopg2-binary or similar for sync fallback if needed, BUT my requirements.txt ONLY has asyncpg.
        # So I MUST use asyncpg or add psycopg2. 
        # Let's add 'psycopg2-binary' to requirements if I want sync, or write this as async.
        # I'll write it as async but provide a sync wrapper or just assume async usage.
        
        # Actually, let's just log to structured logs for now and assume a separate background process 
        # or generic DB writer handles the DB insert to avoid latency in the main path.
        # BUT the plan says "AuditLogger: writes DataLineage records". 
        # "TraceLog" table exists. 
        
        # Let's write a simple async logger.
        self.db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        self.engine = create_async_engine(self.db_url, echo=False)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def log_trace(self, trace_id: str, stage: ProcessingStage, status: TraceStatus, message: str = None, metadata: dict = None):
        """
        Log a trace event to the database.
        """
        logger.info("audit_log", trace_id=trace_id, stage=stage, status=status, message=message)
        
        async with self.async_session() as session:
            try:
                # Use raw SQL or model insert. Using raw SQL for minimal dependency on exact model mapping details here if models.py changes.
                # But better to use the Pydantic model or ORM.
                # Since I didn't set up ORM mappers (just Pydantic models), I will use raw SQL for speed/simplicity in this phase.
                from sqlalchemy import text
                
                query = text("""
                    INSERT INTO trace_logs (trace_id, stage, status, message, metadata)
                    VALUES (:trace_id, :stage, :status, :message, :metadata)
                """)
                
                await session.execute(query, {
                    "trace_id": trace_id,
                    "stage": stage.value,
                    "status": status.value,
                    "message": message,
                    "metadata": json.dumps(metadata) if metadata else None
                })
                await session.commit()
            except Exception as e:
                logger.error("audit_log_persist_failed", error=str(e), trace_id=trace_id)

audit_logger = AuditLogger()
