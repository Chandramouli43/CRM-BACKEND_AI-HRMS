# app/routers/leads.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlmodel import Session

from app.schemas import lead
from .. import crud
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[lead.LeadRead])
def read_leads(skip: int = 0, limit: int = Query(100, le=1000), session: Session = Depends(get_db)):
    return crud.get_leads(session, skip=skip, limit=limit)

@router.get("/{lead_id}", response_model=lead.LeadRead)
def read_lead(lead_id: int, session: Session = Depends(get_db)):
    lead = crud.get_lead(session, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.post("/", response_model=lead.LeadRead, status_code=201)
def create_lead(lead_in: lead.LeadCreate, session: Session = Depends(get_db)):
    return crud.create_lead(session, lead_in)

@router.put("/{lead_id}", response_model=lead.LeadRead)
def update_lead(lead_id: int, lead_in: lead.LeadUpdate, session: Session = Depends(get_db)):
    updated = crud.update_lead(session, lead_id, lead_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Lead not found")
    return updated

@router.delete("/{lead_id}", status_code=204)
def delete_lead(lead_id: int, session: Session = Depends(get_db)):
    ok = crud.delete_lead(session, lead_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Lead not found")
    return None
