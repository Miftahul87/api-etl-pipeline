from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Float, Integer, Text, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
def utcnow(): return datetime.now(timezone.utc)
class PipelineRun(Base):
    __tablename__="pipeline_runs"
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    status: Mapped[str]=mapped_column(String(20),default="PENDING",index=True)
    started_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
    finished_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
    extracted_count: Mapped[int]=mapped_column(Integer,default=0)
    loaded_count: Mapped[int]=mapped_column(Integer,default=0)
    rejected_count: Mapped[int]=mapped_column(Integer,default=0)
    error_message: Mapped[str|None]=mapped_column(Text,nullable=True)
class ETLRecord(Base):
    __tablename__="etl_records"
    __table_args__=(UniqueConstraint("external_id",name="uq_etl_external_id"),)
    id: Mapped[int]=mapped_column(Integer,primary_key=True)
    external_id: Mapped[str]=mapped_column(String(120),index=True)
    name: Mapped[str]=mapped_column(String(240))
    email: Mapped[str|None]=mapped_column(String(320),nullable=True)
    amount: Mapped[float|None]=mapped_column(Float,nullable=True)
    source_updated_at: Mapped[str|None]=mapped_column(String(80),nullable=True)
    payload: Mapped[dict]=mapped_column(JSON)
    loaded_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow,onupdate=utcnow)
