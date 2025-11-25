from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.core.database import get_db
from app import schemas
from app import models, crud

router = APIRouter()


# -----------------------------
# Deals Analytics
# -----------------------------

@router.get("/deals", response_model=List[schemas.DealOut])
def list_deals(db: Session = Depends(get_db), q: Optional[str] = None):
    query = db.query(models.Deal)
    if q:
        query = query.filter(models.Deal.deal_name.ilike(f"%{q}%"))
    return query.all()


@router.get("/deals/{deal_id}", response_model=schemas.DealOut)
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


# -----------------------------
# Leads Analytics
# -----------------------------

@router.get("/leads", response_model=List[schemas.LeadRead])
def read_leads(skip: int = 0, limit: int = Query(100, le=1000), db: Session = Depends(get_db)):
    return crud.get_leads(db, skip=skip, limit=limit)


@router.get("/leads/{lead_id}", response_model=schemas.LeadRead)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = crud.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


# -----------------------------
# Contacts Analytics
# -----------------------------

@router.get("/contacts-by-role")
def contacts_by_role(db: Session = Depends(get_db)):
    if hasattr(models.Contact, "role"):
        rows = (
            db.query(models.Contact.role, func.count(models.Contact.id))
            .group_by(models.Contact.role)
            .all()
        )
        return [{"role": r[0] or "Unknown", "count": r[1]} for r in rows]
    total = db.query(func.count(models.Contact.id)).scalar() or 0
    return [{"role": "N/A", "count": total}]


@router.get("/recent-contacts", response_model=List[schemas.ContactBase])
def recent_contacts(limit: int = 10, db: Session = Depends(get_db)):
    if hasattr(models.Contact, "created_at"):
        return (
            db.query(models.Contact)
            .order_by(models.Contact.created_at.desc())
            .limit(limit)
            .all()
        )
    return db.query(models.Contact).limit(limit).all()


# -----------------------------
# Companies Analytics
# -----------------------------

@router.get("/recent-companies", response_model=List[schemas.CompanyBase])
def recent_companies(limit: int = 10, db: Session = Depends(get_db)):
    if hasattr(models.Company, "created_at"):
        return (
            db.query(models.Company)
            .order_by(models.Company.created_at.desc())
            .limit(limit)
            .all()
        )
    return db.query(models.Company).limit(limit).all()


@router.get("/companies-by-month")
def companies_by_month(db: Session = Depends(get_db)):
    if hasattr(models.Company, "created_at"):
        rows = (
            db.query(
                func.date_trunc("month", models.Company.created_at),
                func.count(models.Company.id)
            )
            .group_by(func.date_trunc("month", models.Company.created_at))
            .order_by(func.date_trunc("month", models.Company.created_at))
            .all()
        )
        return [{"month": str(r[0].date()), "count": r[1]} for r in rows]

    total = db.query(func.count(models.Company.id)).scalar() or 0
    return [{"month": "N/A", "count": total}]


# -----------------------------
# Activities Analytics
# -----------------------------

@router.get("/activities", response_model=List[schemas.Activity])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return crud.get_activities(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent-activities", response_model=List[schemas.Activity])
def recent_activities(limit: int = 10, db: Session = Depends(get_db)):
    if hasattr(models.Activity, "created_at"):
        return (
            db.query(models.Activity)
            .order_by(models.Activity.created_at.desc())
            .limit(limit)
            .all()
        )
    return db.query(models.Activity).limit(limit).all()
