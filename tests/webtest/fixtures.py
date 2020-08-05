import pytest
from flask_webtest import TestApp

from c3bottles import app
from c3bottles.model.user import User

name = "foobar"
password = "secure_password123"

testapp = TestApp(app)


@pytest.fixture
def fresh_state():
    testapp.reset()


@pytest.fixture
def with_admin_user():
    testapp.reset()
    User(name, password, is_admin=True)

    res = testapp.get("/")
    form = res.forms["login_form"]
    form["username"] = name
    form["password"] = password
    form.submit()

    return name, password


@pytest.fixture
def with_regular_user():
    testapp.reset()
    User(name, password)
    res = testapp.get("/")
    form = res.forms["login_form"]
    form["username"] = name
    form["password"] = password
    form.submit()

    return name, password
