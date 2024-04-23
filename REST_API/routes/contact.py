from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..repository import contact as contact_repository
from ..schemas import Contact, ContactCreate, ContactUpdate,UserModel
from datetime import date, timedelta
from ..services.auth import Auth
from ..database.models import User 


router = APIRouter(prefix='/contact', tags=["contact"])

@router.get("/", response_model=list[Contact])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db:Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
    ):
    return contact_repository.get_contacts(current_user, db, skip, limit)

@router.get("/{contact_id}", response_model=Contact)
async def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
):
    db_contact = contact_repository.get_contact(current_user, db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.post("/", response_model=Contact)
async def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
):
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
    return contact_repository.search_contacts(current_user, db, query)

@router.get("/birthdays/", response_model=list[Contact])
async def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(Auth.get_current_user)
):
    return contact_repository.get_upcoming_birthdays(current_user, db)
