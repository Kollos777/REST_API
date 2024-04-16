from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..repository import contact as contact_repository
from ..schemas import Contact, ContactCreate, ContactUpdate
from datetime import date, timedelta

router = APIRouter(prefix='/contact', tags=["contact"])

@router.get("/", response_model=list[Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return contact_repository.get_contacts(db, skip, limit)

@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = contact_repository.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = contact_repository.create_contact(db, contact)
    if db_contact is None:
        raise HTTPException(status_code=400, detail="Failed to create contact")
    return db_contact

@router.put("/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = contact_repository.update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = contact_repository.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/search/", response_model=list[Contact])
def search_contacts(query: str = None, db: Session = Depends(get_db)):
    return contact_repository.search_contacts(db, query)

@router.get("/birthdays/", response_model=list[Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    return contact_repository.get_upcoming_birthdays(db)

