from sqlalchemy.orm import Session
from ..database import models
from ..schemas import ContactCreate, ContactUpdate

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = models.Contact(
        **contact.dict()
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        return None
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact is None:
        return None
    db.delete(db_contact)
    db.commit()
    return db_contact

def search_contacts(db: Session, query: str = None):
    if not query:
        return db.query(models.Contact).all()

    search_query = f"%{query}%"
    return db.query(models.Contact).filter(
        models.Contact.first_name.ilike(search_query) |
        models.Contact.last_name.ilike(search_query) |
        models.Contact.email.ilike(search_query)
    ).all()

def get_upcoming_birthdays(db: Session):
    from datetime import date, timedelta
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.birthday.between(today, next_week)
    ).all()