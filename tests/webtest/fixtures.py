from pytest import fixture

from flask_webtest import TestApp
from flask_webtest import SessionScope

from c3bottles import app, db
from c3bottles.model.user import User


name = "foobar"
password = "secure_password123"

testapp = TestApp(app)


def db_setup():
    db.engine.execute("ATTACH ':memory:' AS meta;")
    db.create_all()


def db_teardown():
    db.drop_all()
    db.engine.execute("DETACH meta;")


@fixture
def fresh_state(request):
    testapp.reset()
    with SessionScope(db):
        db_setup()

    def fin():
        with SessionScope(db):
            db_teardown()
    request.addfinalizer(fin)


@fixture
def with_admin_user(request):
    testapp.reset()
    with SessionScope(db):
        db_setup()
        user = User(name, password, is_admin=True)
        db.session.add(user)
        db.session.commit()

    def fin():
        with SessionScope(db):
            db_teardown()
    request.addfinalizer(fin)
    res = testapp.get("/")
    form = res.forms["login_form"]
    form["username"] = name
    form["password"] = password
    form.submit()

    return name, password


@fixture
def with_regular_user(request):
    with SessionScope(db):
        db_setup()
        user = User(name, password)
        db.session.add(user)
        db.session.commit()

    def fin():
        with SessionScope(db):
            db_teardown()
    request.addfinalizer(fin)
    testapp.reset()
    res = testapp.get("/")
    form = res.forms["login_form"]
    form["username"] = name
    form["password"] = password
    form.submit()

    return name, password
