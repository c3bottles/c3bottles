import pytest

from c3bottles import db


@pytest.fixture(scope="function", autouse=True)
def database(request):
    db.engine.execute("ATTACH ':memory:' AS meta;")
    db.create_all()

    def fin():
        db.drop_all()
        db.engine.execute("DETACH meta;")

    request.addfinalizer(fin)
