import pytest
from sqlalchemy import text

from c3bottles import app, db


@pytest.fixture(scope="function", autouse=True)
def app_ctx():
    with app.app_context():
        yield


@pytest.fixture(scope="function", autouse=True)
def request_ctx():
    with app.test_request_context():
        yield


@pytest.fixture(scope="function", autouse=True)
def database(request):
    db.session.execute(text("ATTACH ':memory:' AS meta;"))
    db.create_all()

    def fin():
        db.drop_all()
        db.session.execute(text("DETACH meta;"))

    request.addfinalizer(fin)
