from typing import List
from sqlalchemy.orm import Session
from ..database.models import Contact,User
from ..schemas import ContactCreate, ContactUpdate
from sqlalchemy import and_

def get_contacts(user: User,db: Session, skip: int = 0, limit: int = 100)-> List[Contact]:
    """
    Retrieves a list of contacts for the specified user with pagination.

    :param user: The user whose contacts are being retrieved.
    :type user: User
    :param db: The database session.
    :type db: Session
    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == User.id).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    """
    Retrieves a single contact with the specified ID.

    :param db: The database session.
    :type db: Session
    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :return: The contact with the specified ID, or None if not found.
    """
    return db.query(Contact).and_filter(Contact.id == contact_id,Contact.user_id == User.id).first()

def create_contact(user: User,db: Session, contact: ContactCreate):
    """
    Creates a new contact for the specified user.

    :param user: The user for whom the contact is being created.
    :type user: User
    :param db: The database session.
    :type db: Session
    :param contact: The data for the new contact.
    :type contact: ContactCreate
    :return: The newly created contact.
    """
    db_contact = Contact(
        **contact.dict(), user_id = user.id
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(user: User, db: Session, contact_id: int, contact: ContactUpdate):
    """
    Updates an existing contact for the specified user.

    :param user: The user who owns the contact.
    :type user: User
    :param db: The database session.
    :type db: Session
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param contact: The updated data for the contact.
    :type contact: ContactUpdate
    :return: The updated contact, or None if not found.
    """
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id == user.id)).first()
    if db_contact is None:
        return None
    for key, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(user: User,db: Session, contact_id: int):
    """
    Deletes a contact for the specified user.

    :param user: The user who owns the contact.
    :type user: User
    :param db: The database session.
    :type db: Session
    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :return: The deleted contact, or None if not found.
    """
    db_contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id == user.id)).first()
    if db_contact is None:
        return None
    db.delete(db_contact)
    db.commit()
    return db_contact

def search_contacts(user: User,db: Session, query: str = None):
    """
    Searches contacts for the specified user by a given query.

    :param user: The user whose contacts are being searched.
    :type user: User
    :param db: The database session.
    :type db: Session
    :param query: The search query.
    :type query: str
    :return: A list of contacts matching the query.
    """
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
    """
    Retrieves upcoming birthdays for the specified user.

    :param user: The user whose contacts' birthdays are being checked.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts with birthdays in the next week.
    """
    from datetime import date, timedelta
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(
        (Contact.birthday.between(today, next_week)) &
        (Contact.user_id == user.id)
    ).all()
