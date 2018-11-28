import pytest

from flask import url_for

from c3bottles import c3bottles
from .fixtures import testapp, fresh_state


@pytest.mark.parametrize("view", ["index", "faq", "dp_list", "dp_map", "statistics.html"])
def test_basic_views(view, fresh_state):
    with c3bottles.test_request_context():
        res = testapp.get(url_for(view))
    assert res.status_int == 200


def test_404(fresh_state):
    res = testapp.get("/nonexistant", expect_errors=True)
    assert res.status_int == 404
    assert "Not found" in res


def test_admin_area_401_index(fresh_state):
    with c3bottles.test_request_context():
        res = testapp.get(url_for("admin.index"), expect_errors=True)
    assert res.status_int == 401
    assert "Unauthorized" in res


def test_admin_area_401_always(fresh_state):
    with c3bottles.test_request_context():
        res = testapp.get(url_for("admin.index") + "/nonexistant", expect_errors=True)
    assert res.status_int == 401
    assert "Unauthorized" in res
