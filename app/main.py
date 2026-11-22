from fastapi import FastAPI,Depends,BackgroundTasks,HTTPException,Query
from sqlalchemy.orm import Session
from sqlalchemy import select,desc
from .database import Base,engine,get_db
from .models import PipelineRun,ETLRecord
from .schemas import TriggerResponse,RunResponse,RecordResponse
from .pipeline import execute_pipeline
from .mock_source import router as mock_router
app=FastAPI(title="API Data Integration & ETL Pipeline",version="1.0.0",
 description="Paginated REST extraction, validation, normalization and idempotent PostgreSQL loading.")
Base.metadata.create_all(bind=engine)
app.include_router(mock_router)
@app.get("/health")
def health(db:Session=Depends(get_db)):
    try: db.execute(select(1)); return {"status":"ok","database":"connected"}
    except Exception as exc: raise HTTPException(503,detail="Database unavailable") from exc
@app.post("/trigger",response_model=TriggerResponse,status_code=202)
def trigger(background_tasks:BackgroundTasks,db:Session=Depends(get_db)):
    latest=db.scalar(select(PipelineRun).where(PipelineRun.status.in_(["PENDING","RUNNING"])).order_by(desc(PipelineRun.id)))
    if latest: raise HTTPException(409,detail=f"Pipeline run {latest.id} is already {latest.status.lower()}.")
    run=PipelineRun(status="PENDING"); db.add(run); db.commit(); db.refresh(run)
    background_tasks.add_task(execute_pipeline,run.id)
    return TriggerResponse(run_id=run.id,status=run.status,message="Pipeline accepted for background execution.")
@app.get("/status",response_model=RunResponse)
def status(db:Session=Depends(get_db)):
    run=db.scalar(select(PipelineRun).order_by(desc(PipelineRun.id)))
    if not run: raise HTTPException(404,detail="No pipeline run found. Trigger a run first.")
    return run
@app.get("/runs",response_model=list[RunResponse])
def runs(limit:int=Query(20,ge=1,le=100),db:Session=Depends(get_db)):
    return list(db.scalars(select(PipelineRun).order_by(desc(PipelineRun.id)).limit(limit)))
@app.get("/records",response_model=list[RecordResponse])
def records(limit:int=Query(50,ge=1,le=500),offset:int=Query(0,ge=0),db:Session=Depends(get_db)):
    return list(db.scalars(select(ETLRecord).order_by(ETLRecord.external_id).offset(offset).limit(limit)))
