import unittest
from unittest.mock import MagicMock
from datetime import date, timedelta

from sqlalchemy.orm import Session

from REST_API.database.models import Contact, User
from REST_API.schemas import ContactCreate, ContactUpdate, Contact
from REST_API.repository.contact import (
    get_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_upcoming_birthdays,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(user=self.user, db=self.session, skip=0, limit=10)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(db=self.session, contact_id=1)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(db=self.session, contact_id=1)
        self.assertIsNone(result)

    async def test_create_contact(self):
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "birthday": date.today(),
        }
        contact_create = ContactCreate(**contact_data)
        contact = Contact(**contact_data, user_id=self.user.id)
        result = await create_contact(user=self.user, db=self.session, contact=contact_create)
        self.assertEqual(result, contact)

    async def test_update_contact_found(self):
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "birthday": date.today(),
        }
        contact_update = ContactUpdate(**contact_data)
        contact = Contact(**contact_data, user_id=self.user.id)
        self.session.query().filter().first.return_value = contact
        result = await update_contact(user=self.user, db=self.session, contact_id=1, contact=contact_update)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        contact_update = ContactUpdate(first_name="John", last_name="Doe")
        self.session.query().filter().first.return_value = None
        result = await update_contact(user=self.user, db=self.session, contact_id=1, contact=contact_update)
        self.assertIsNone(result)

    async def test_delete_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await delete_contact(user=self.user, db=self.session, contact_id=1)
        self.assertEqual(result, contact)

    async def test_delete_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await delete_contact(user=self.user, db=self.session, contact_id=1)
        self.assertIsNone(result)

    async def test_search_contacts(self):
        query = "John"
        contacts = [Contact(first_name="John"), Contact(first_name="Johnny")]
        self.session.query().filter().all.return_value = contacts
        result = await search_contacts(user=self.user, db=self.session, query=query)
        self.assertEqual(result, contacts)

    async def test_get_upcoming_birthdays(self):
        today = date.today()
        next_week = today + timedelta(days=7)
        birthdays = [Contact(birthday=today), Contact(birthday=next_week)]
        self.session.query().filter().all.return_value = birthdays
        result = await get_upcoming_birthdays(user=self.user, db=self.session)
        self.assertEqual(result, birthdays)


if __name__ == '__main__':
    unittest.main()

