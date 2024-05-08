import unittest
from unittest.mock import MagicMock

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from REST_API.database.models import User
from REST_API.schemas import UserModel,UserDb,UserResponse
from REST_API.repository.auth import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestAuthService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)

    async def test_get_user_by_email(self):
        email = "test@example.com"
        user = User(email=email)
        self.db.query().filter().first.return_value = user
        result = await get_user_by_email(email, self.db)
        self.assertEqual(result, user)

    async def test_create_user(self):
        email = "test@example.com"
        body = UserModel(email=email)
        new_user = User(**body.dict())
        result = await create_user(body, self.db)
        self.assertEqual(result, new_user)

    async def test_update_token(self):
        user = User()
        token = "test_token"
        update_token(user, token, self.db)
        self.assertEqual(user.refresh_token, token)

    async def test_confirmed_email(self):
        email = "test@example.com"
        user = User(email=email)
        self.db.query().filter().first.return_value = user
        confirmed_email(email, self.db)
        self.assertTrue(user.confirmed)

    async def test_update_avatar(self):
        email = "test@example.com"
        user = User(email=email)
        url = "http://example.com/avatar.jpg"
        self.db.query().filter().first.return_value = user
        result = await update_avatar(email, url, self.db)
        self.assertEqual(result.avatar, url)


if __name__ == '__main__':
    unittest.main()