from pydantic import BaseModel
from datetime import date
from typing import Optional

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_info: Optional[str]

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        from_attributes = True
