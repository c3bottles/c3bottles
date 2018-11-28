from pytest import fixture

from flask_webtest import TestApp
from flask_webtest import SessionScope

from c3bottles import c3bottles, db
from c3bottles.model.user import User


name = "foobar"
password = "secure_password123"

testapp = TestApp(c3bottles)


@fixture
def fresh_state():
    testapp.reset()


@fixture
def with_admin_user(request):
    testapp.reset()
    with SessionScope(db):
        db.engine.execute("ATTACH ':memory:' AS meta;")
        db.create_all()
        user = User(name, password, is_admin=True)
        db.session.add(user)
        db.session.commit()

    def fin():
        with SessionScope(db):
            db.drop_all()
            db.engine.execute("DETACH meta;")
    request.addfinalizer(fin)
    res = testapp.get("/login")
    form = res.forms["login_form"]
    form["username"] = name
    form["password"] = password
    form.submit()

    return name, password


@fixture
def with_regular_user(request):
    with SessionScope(db):
        db.engine.execute("ATTACH ':memory:' AS meta;")
        db.create_all()
        user = User(name, password)
        db.session.add(user)
        db.session.commit()

    def fin():
        with SessionScope(db):
            db.drop_all()
            db.engine.execute("DETACH meta;")
    request.addfinalizer(fin)
    testapp.reset()
    res = testapp.get("/login")
    form = res.forms["login_form"]
    form["username"] = name
    form["password"] = password
    form.submit()

    return name, password
