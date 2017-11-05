import pytest

from c3bottles.model.user import User

from test import C3BottlesTestCase, NAME, PASSWORD


class UserTestCase(C3BottlesTestCase):

    def test_create_user(self):
        user = self.create_test_user()

        self.assertEqual(user.name, NAME)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.can_edit, False)
        self.assertEqual(user.can_visit, True)

    def test_create_created_edit(self):
        user = User(NAME, PASSWORD, can_edit=True)
        created = self.create_user(user)

        self.assertEqual(created.name, NAME)
        self.assertEqual(created.is_active, True)
        self.assertEqual(created.is_admin, False)
        self.assertEqual(created.can_edit, True)
        self.assertEqual(created.can_visit, True)

    def test_create_user_admin(self):
        user = User(NAME, PASSWORD, is_admin=True)
        created = self.create_user(user)

        self.assertEqual(created.name, NAME)
        self.assertEqual(created.is_active, True)
        self.assertEqual(created.is_admin, True)
        self.assertEqual(created.can_edit, False)
        self.assertEqual(created.can_visit, True)

    def test_create_user_invalid(self):
        with pytest.raises(ValueError) as err:
            User(NAME, '')
        assert 'User needs a name and a password' in str(err)
        assert 'Password hashing failed' in str(err)

        with pytest.raises(ValueError) as err:
            User('', PASSWORD)
        assert 'User needs a name and a password' in str(err)

        with pytest.raises(ValueError) as err:
            User(NAME * 33, PASSWORD)
        assert 'User name is too long' in str(err)

        with pytest.raises(ValueError) as err:
            User(33, PASSWORD)
        assert 'User name is not a string' in str(err)

    def test_validate_password(self):
        user = self.create_test_user()

        self.assertFalse(user.validate_password(NAME))
        self.assertTrue(user.validate_password(PASSWORD))

    def test_get_by_token(self):
        self.assertIsNone(User.get_by_token(NAME))

        user = User(NAME, PASSWORD)
        created = self.create_user(user)

        self.assertIsNone(User.get_by_token(NAME))
        self.assertEqual(User.get_by_token(created.get_id()), created)

    def test_get_all(self):
        self.assertEqual(User.all(), [])

        user = User(NAME, PASSWORD)
        created = self.create_user(user)

        self.assertEqual(User.all(), [created])
