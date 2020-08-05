from c3bottles import app

from .test_user import password, user, username  # noqa


def test_login_fail(user):
    resp = app.test_client().post(
        "/login", data=dict(username=username, password="foo"), follow_redirects=True
    )
    assert resp.status_code == 200
    assert "Wrong user name or password" in str(resp.data)


def test_login_success(user):
    resp = app.test_client().post(
        "/login", data=dict(username=username, password=password), follow_redirects=True
    )
    assert resp.status_code == 200
    assert "Wrong user name or password" not in str(resp.data)
