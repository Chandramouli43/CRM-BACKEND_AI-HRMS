# app/routers/contacts.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os

from app.schemas import contact
from app.core.database import get_db
from .. import crud
from app.models import Contact as ContactModel

router = APIRouter()

# Upload directory
UPLOAD_FOLDER = "uploads/profiles"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------- UTIL: Convert DB Model → Frontend JSON ---------------------- #
def convert_contact_output(db_contact: ContactModel):
    """Convert DB fields into frontend-friendly structure."""
    if not db_contact:
        return None

    contact_dict = db_contact.__dict__.copy()

    # Convert CSV → list
    if db_contact.tags:
        contact_dict["tags"] = db_contact.tags.split(",")
    else:
        contact_dict["tags"] = []

    # Ensure profile_photo is URL-friendly
    if db_contact.profile_photo:
        contact_dict["profile_photo"] = f"/{db_contact.profile_photo}"
    else:
        contact_dict["profile_photo"] = None

    # Remove SQLAlchemy internal key
    contact_dict.pop("_sa_instance_state", None)

    return contact_dict


# -------------------- CREATE CONTACT -------------------- #
@router.post("/", response_model=contact.ContactResponse)
def create_contact(contact_data: contact.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.create_contact(db=db, contact=contact_data)
    return convert_contact_output(db_contact)


# -------------------- READ ALL CONTACTS -------------------- #
@router.get("/", response_model=List[contact.ContactResponse])
def read_contacts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    db_contacts = crud.get_contacts(db=db, skip=skip, limit=limit)
    return [convert_contact_output(c) for c in db_contacts]


# -------------------- READ SINGLE CONTACT -------------------- #
@router.get("/{contact_id}", response_model=contact.ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return convert_contact_output(db_contact)


# -------------------- UPDATE CONTACT -------------------- #
@router.put("/{contact_id}", response_model=contact.ContactResponse)
def update_contact(contact_id: int, updated: contact.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db=db, contact_id=contact_id, updated=updated)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return convert_contact_output(db_contact)


# -------------------- DELETE CONTACT -------------------- #
@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_contact(db=db, contact_id=contact_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"detail": "Contact deleted successfully"}


# -------------------- UPDATE PROFILE PHOTO -------------------- #
@router.put("/{contact_id}/profile-photo")
def update_profile_photo(
    contact_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db_contact = db.query(ContactModel).filter(ContactModel.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    # Save file
    file_path = f"{UPLOAD_FOLDER}/profile_{contact_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Update DB
    db_contact.profile_photo = file_path
    db.commit()
    db.refresh(db_contact)

    return {
        "message": "Profile photo updated successfully",
        "profile_photo": f"/{file_path}"
    }
