from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from REST_API.database.db import get_db
from REST_API.schemas import Contact, ContactCreate,ContactUpdate
from datetime import date, timedelta

router = APIRouter(prefix='/contact', tags=["contact"])


@router.get("/", response_model=list[Contact])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Contact).offset(skip).limit(limit).all()


@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.put("/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete("/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return db_contact


@router.get("/search/", response_model=list[Contact])
def search_contacts(query: str = None, db: Session = Depends(get_db)):
    if not query:
        return db.query(Contact).all()

    search_query = f"%{query}%"
    return db.query(Contact).filter(
        Contact.first_name.ilike(search_query) |
        Contact.last_name.ilike(search_query) |
        Contact.email.ilike(search_query)
    ).all()

@router.get("/birthdays/", response_model=list[Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(
        Contact.birthday.between(today, next_week)
    ).all()

