import pytest

from c3bottles import db
from c3bottles.model.user import User

username = "user"
password = "password"


@pytest.fixture
def user():
    db.session.expunge_all()
    return User(name=username, password=password)


@pytest.fixture
def editor():
    db.session.expunge_all()
    return User(name=username, password=password, can_edit=True)


@pytest.fixture
def admin():
    db.session.expunge_all()
    return User(name=username, password=password, is_admin=True)


def test_user_name(user):
    assert user.name == username


def test_user_active(user):
    assert user.is_active


def test_user_not_admin(user):
    assert not user.is_admin


def test_user_cant_edit(user):
    assert not user.can_edit


def test_user_can_visit(user):
    assert user.can_visit


def test_editor_name(editor):
    assert editor.name == username


def test_editor_is_active(editor):
    assert editor.is_active


def test_editor_not_admin(editor):
    assert not editor.is_admin


def test_editor_can_edit(editor):
    assert editor.can_edit


def test_editor_can_visit(editor):
    assert editor.can_visit


def test_admin_name(admin):
    assert admin.name == username


def test_admin_is_active(admin):
    assert admin.is_active


def test_admin_is_admin(admin):
    assert admin.is_admin


def test_admin_cant_edit(admin):
    assert not admin.can_edit


def test_admin_can_visit(admin):
    assert admin.can_visit


def test_create_user_no_password():
    with pytest.raises(ValueError) as err:
        User(username, "")
    assert "User needs a name and a password" in str(err.value)
    assert "Password hashing failed" in str(err.value)


def test_create_user_no_name():
    with pytest.raises(ValueError, match="User needs a name and a password"):
        User("", password)


def test_user_name_too_long():
    with pytest.raises(ValueError, match="User name is too long"):
        User(username * 33, password)


def test_invalid_username():
    with pytest.raises(ValueError, match="User name is not a string"):
        User(33, password)  # noqa


def test_validate_password(user):
    assert user.validate_password(password)


def test_wrong_password(user):
    assert not user.validate_password("foo")


def test_get_by_token(user):
    assert User.get_by_token(user.get_id()) == user


def test_get_by_wrong_token(user):
    assert User.get_by_token(username) is None


def test_get_all(user):
    assert User.all() == [user]
