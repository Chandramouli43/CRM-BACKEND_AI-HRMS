# app/routers/pipelines.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import pipeline
from app import models, crud
from app.core.database import get_db

router = APIRouter()

# Dependency: use get_db imported from core.database (do not redefine it here)


@router.post("/", response_model=pipeline.PipelineResponse)
def create_pipeline(pipeline: pipeline.PipelineCreate, db: Session = Depends(get_db)):
    db_pipeline = crud.create_pipeline(db=db, pipeline=pipeline)
    return db_pipeline


@router.get("/", response_model=List[pipeline.PipelineResponse])
def read_pipelines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pipelines(db, skip=skip, limit=limit)


@router.delete("/{pipeline_id}")
def delete_pipeline(pipeline_id: int, db: Session = Depends(get_db)):
    success = crud.delete_pipeline(db, pipeline_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return {"ok": True}
