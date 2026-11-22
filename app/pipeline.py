from datetime import datetime, timezone
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import PipelineRun
from .extract import fetch_all_pages
from .transform import transform_records
from .load import upsert_records
def execute_pipeline(run_id:int):
    db:Session=SessionLocal()
    run=db.get(PipelineRun,run_id)
    if run is None: db.close(); return
    run.status="RUNNING"; db.commit()
    try:
        raw=fetch_all_pages()
        transformed=transform_records(raw)
        loaded=upsert_records(db,transformed.accepted)
        run.extracted_count=len(raw); run.loaded_count=loaded
        run.rejected_count=transformed.rejected; run.status="SUCCEEDED"
    except Exception as exc:
        db.rollback()
        run=db.get(PipelineRun,run_id)
        run.status="FAILED"; run.error_message=str(exc)[:2000]
    finally:
        run=db.get(PipelineRun,run_id)
        run.finished_at=datetime.now(timezone.utc)
        db.commit(); db.close()
