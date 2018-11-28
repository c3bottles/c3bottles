from .fixtures import testapp, fresh_state


def test_index(fresh_state):
    res = testapp.get("/")
    assert res.status_int == 200
