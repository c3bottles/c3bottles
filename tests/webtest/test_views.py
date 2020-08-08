import pytest
from flask import url_for

from c3bottles import app
from c3bottles.config.map import MapSource

from .fixtures import fresh_state, testapp  # noqa

basic_views = ["main.index", "main.faq", "view.list_", "statistics.numbers"]


@pytest.mark.parametrize("view", basic_views)
def test_basic_views(view, fresh_state):
    with app.test_request_context():
        res = testapp.get(url_for(view))
    assert res.status_int == 200


def test_map_view(fresh_state):
    with app.test_request_context():
        res = testapp.get(url_for("view.map_"), expect_errors=True)
    assert res.status_int == 404
    assert "Not found" in res
    app.config["MAP_SOURCE"] = MapSource
    with app.test_request_context():
        res = testapp.get(url_for("view.map_"))
    assert res.status_int == 200


def test_404(fresh_state):
    res = testapp.get("/nonexistant", expect_errors=True)
    assert res.status_int == 404
    assert "Not found" in res


def test_admin_area_401_index(fresh_state):
    with app.test_request_context():
        res = testapp.get(url_for("admin.index"), expect_errors=True)
    assert res.status_int == 401
    assert "Unauthorized" in res


def test_admin_area_401_always(fresh_state):
    with app.test_request_context():
        res = testapp.get(url_for("admin.index") + "/nonexistant", expect_errors=True)
    assert res.status_int == 401
    assert "Unauthorized" in res
