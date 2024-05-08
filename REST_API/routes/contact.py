from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..repository import contact as contact_repository
from ..schemas import Contact, ContactCreate, ContactUpdate, UserModel
from datetime import date, timedelta
from ..services.auth import Auth
from ..database.models import User
from typing import List
from fastapi_limiter import FastAPILimiter, RateLimiter


router = APIRouter(prefix='/contact', tags=["contact"])

@router.get("/", response_model=List[Contact], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db:Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
    ):
    """
    Retrieves a list of contacts for the current user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return contact_repository.get_contacts(current_user, db, skip, limit)

@router.get("/{contact_id}", response_model=Contact)
async def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
):
    """
    Retrieves a single contact with the specified ID for the current user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The contact with the specified ID.
    :rtype: Contact
    """
    db_contact = contact_repository.get_contact(current_user, db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.post("/", response_model=Contact,dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
):
    """
    Creates a new contact for the current user.

    :param contact: The data for the contact to create.
    :type contact: ContactCreate
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The newly created contact.
    :rtype: Contact
    """
    db_contact = contact_repository.create_contact(current_user, db, contact)
    if db_contact is None:
        raise HTTPException(status_code=400, detail="Failed to create contact")
    return db_contact

@router.put("/{contact_id}", response_model=Contact)
async def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
):
    """
    Updates a single contact with the specified ID for the current user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param contact: The updated data for the contact.
    :type contact: ContactUpdate
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The updated contact.
    :rtype: Contact
    """
    db_contact = contact_repository.update_contact(current_user, db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=Contact)
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
):
    """
    Deletes a single contact with the specified ID for the current user.

    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The deleted contact.
    :rtype: Contact
    """
    db_contact = contact_repository.delete_contact(current_user, db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/search/", response_model=list[Contact])
async def search_contacts(
    query: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
):
    """
    Searches for contacts based on the provided query string.

    :param query: The query string to search for.
    :type query: str
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: A list of matching contacts.
    :rtype: List[Contact]
    """
    return contact_repository.search_contacts(current_user, db, query)

@router.get("/birthdays/", response_model=list[Contact])
async def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
):
    """
    Retrieves a list of upcoming birthdays for the current user.

    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: A list of contacts with upcoming birthdays.
    :rtype: List[Contact]
    """
    return contact_repository.get_upcoming_birthdays(current_user, db)
