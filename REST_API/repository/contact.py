from typing import List
from sqlalchemy.orm import Session
from ..database.models import Contact,User
from ..schemas import ContactCreate, ContactUpdate
from sqlalchemy import and_

def get_contacts(user: User,db: Session, skip: int = 0, limit: int = 100)-> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == User.id).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).and_filter(Contact.id == contact_id,Contact.user_id == User.id).first()

def create_contact(user: User,db: Session, contact: ContactCreate):
    db_contact = Contact(
        **contact.dict(), user_id = user.id
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(user: User, db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id == user.id)).first()
    if db_contact is None:
        return None
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(user: User,db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id == user.id)).first()
    if db_contact is None:
        return None
    db.delete(db_contact)
    db.commit()
    return db_contact

def search_contacts(user: User,db: Session, query: str = None):
    if not query:
        return db.query(Contact).all()

    search_query = f"%{query}%"
    return db.query(Contact).filter(
            (Contact.first_name.ilike(search_query) |
            Contact.last_name.ilike(search_query) |
            Contact.email.ilike(search_query)) &
            (Contact.user_id == user.id)
        ).all()

def get_upcoming_birthdays(user: User,db: Session):
    from datetime import date, timedelta
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(
        (Contact.birthday.between(today, next_week)) &
        (Contact.user_id == user.id)
    ).all()