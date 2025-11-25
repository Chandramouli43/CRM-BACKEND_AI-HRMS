from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List 
import os
import shutil

from app.schemas import company
from app.core.database import get_db
from .. import models

router = APIRouter()

UPLOAD_FOLDER = "uploads/logos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------- CREATE -------------------- #
@router.post("/", response_model=company.CompanyResponse)
def create_company(
    company_name: str = Form(...),
    phone_number: str = Form(...),
    phone_number2: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    rating: Optional[float] = Form(None),
    fax: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    owner: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    deals: Optional[str] = Form(None),
    industry: Optional[str] = Form(None),
    source: Optional[str] = Form(None),
    currency: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    about: Optional[str] = Form(None),
    contact: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    zipcode: Optional[str] = Form(None),
    facebook: Optional[str] = Form(None),
    twitter: Optional[str] = Form(None),
    linkedin: Optional[str] = Form(None),
    skype: Optional[str] = Form(None),
    whatsapp: Optional[str] = Form(None),
    instagram: Optional[str] = Form(None),
    visibility: Optional[str] = Form("private"),
    status: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    logo_filename = None

    if logo:
        filename = f"{company_name}_{logo.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(logo.file, f)
        logo_filename = filename

    new_company = models.Company(
        company_name=company_name,
        phone_number=phone_number,
        phone_number2=phone_number2,
        email=email,
        location=location,
        rating=rating,
        fax=fax,
        website=website,
        owner=owner,
        tags=tags,
        deals=deals,
        industry=industry,
        source=source,
        currency=currency,
        language=language,
        about=about,
        contact=contact,
        address=address,
        country=country,
        state=state,
        city=city,
        zipcode=zipcode,
        facebook=facebook,
        twitter=twitter,
        linkedin=linkedin,
        skype=skype,
        whatsapp=whatsapp,
        instagram=instagram,
        visibility=visibility,
        status=status,
        logo=logo_filename,
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


# -------------------- READ ALL -------------------- #
@router.get("/", response_model=List[company.CompanyResponse])
def read_companies(db: Session = Depends(get_db)):
    return db.query(models.Company).all()


# -------------------- READ ONE -------------------- #
@router.get("/{company_id}", response_model=company.CompanyResponse)
def read_company(company_id: int, db: Session = Depends(get_db)):
    company_obj = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company_obj:
        raise HTTPException(status_code=404, detail="Company not found")
    return company_obj


# -------------------- UPDATE -------------------- #
@router.put("/{company_id}", response_model=company.CompanyResponse)
def update_company(
    company_id: int,
    company_name: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    phone_number2: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    rating: Optional[float] = Form(None),
    fax: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    owner: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    deals: Optional[str] = Form(None),
    industry: Optional[str] = Form(None),
    source: Optional[str] = Form(None),
    currency: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    about: Optional[str] = Form(None),
    contact: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    zipcode: Optional[str] = Form(None),
    facebook: Optional[str] = Form(None),
    twitter: Optional[str] = Form(None),
    linkedin: Optional[str] = Form(None),
    skype: Optional[str] = Form(None),
    whatsapp: Optional[str] = Form(None),
    instagram: Optional[str] = Form(None),
    visibility: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    # ---------- LOGO ----------
    if logo:
        filename = f"{company_id}_{logo.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(logo.file, f)
        db_company.logo = filename

    # ---------- FIELDS ----------
    updates = {
        "company_name": company_name,
        "phone_number": phone_number,
        "phone_number2": phone_number2,
        "email": email,
        "location": location,
        "rating": rating,
        "fax": fax,
        "website": website,
        "owner": owner,
        "tags": tags,
        "deals": deals,
        "industry": industry,
        "source": source,
        "currency": currency,
        "language": language,
        "about": about,
        "contact": contact,
        "address": address,
        "country": country,
        "state": state,
        "city": city,
        "zipcode": zipcode,
        "facebook": facebook,
        "twitter": twitter,
        "linkedin": linkedin,
        "skype": skype,
        "whatsapp": whatsapp,
        "instagram": instagram,
        "visibility": visibility,
        "status": status
    }

    for field, value in updates.items():
        if value is not None:
            setattr(db_company, field, value)

    db.commit()
    db.refresh(db_company)
    return db_company


# -------------------- UPDATE LOGO -------------------- #
@router.put("/{company_id}/logo")
def update_company_logo(
    company_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    logo_path = f"{UPLOAD_FOLDER}/company_{company_id}_{file.filename}"

    with open(logo_path, "wb") as f:
        f.write(file.file.read())

    db_company.logo = logo_path
    db.commit()
    db.refresh(db_company)

    return {"message": "Logo updated", "logo": logo_path}


# -------------------- DELETE -------------------- #
@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(db_company)
    db.commit()

    return {"message": "Company deleted successfully"}
