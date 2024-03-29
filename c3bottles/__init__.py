import sys

from babel import Locale
from flask import Flask, g, request, session
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_compress import Compress
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from pwgen import pwgen
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_folder="../static", template_folder="../templates")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

if "pytest" not in sys.modules:
    try:
        import config

        app.config.from_object(config)
    except ImportError:
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///c3bottles.db",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SECRET_KEY=pwgen(64),
            BABEL_TRANSLATION_DIRECTORIES="../translations",
        )
        print(
            "\nWARNING: c3bottles is not configured properly and this\n"
            "instance fell back to the default configuration. This means\n"
            "that the secret key will change on every restart of the\n"
            "server and all users will be logged out forcibly!\n"
        )
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SECRET_KEY"] = "secret"

Compress(app)

db = SQLAlchemy(app)
lm = LoginManager(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
babel = Babel(app)

languages = ("en", "de")
locales = {lang: Locale(lang) for lang in languages}
language_list = sorted((lang for lang in languages), key=lambda k: locales[k].get_display_name())


def get_locale() -> str:
    """
    Get the locale from the session. If no locale is available, set it.
    """
    if "lang" not in session or session["lang"] not in language_list:
        set_locale()
    return session["lang"]


def set_locale() -> None:
    """
    Set the locale in the session to one of the available languages.
    If a language has been given via the URL, it is set if it is a valid
    language. If no language has been given via the URL and no language
    is present in the session, the default language will be determined
    according to what the user's browser prefers.
    """
    if "lang" in request.args and request.args["lang"] in language_list:
        session["lang"] = request.args["lang"]
    if "lang" not in session or session["lang"] not in language_list:
        session["lang"] = request.accept_languages.best_match(language_list)
        if session["lang"] is None:
            session["lang"] = "en"
    g.languages, g.locales = language_list, locales


babel.init_app(app, locale_selector=get_locale)
app.before_request(set_locale)

# Trim and strip blocks in jinja2 so no unnecessary
# newlines and tabs appear in the output:
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

from c3bottles.views.action import bp as bp_action  # noqa  # isort:skip
from c3bottles.views.admin import bp as bp_admin  # noqa  # isort:skip
from c3bottles.views.api import bp as bp_api  # noqa  # isort:skip
from c3bottles.views.label import bp as bp_label  # noqa  # isort:skip
from c3bottles.views.main import bp as bp_main  # noqa  # isort:skip
from c3bottles.views.manage import bp as bp_manage  # noqa  # isort:skip
from c3bottles.views.statistics import bp as bp_stats  # noqa  # isort:skip
from c3bottles.views.user import bp as bp_user  # noqa  # isort:skip
from c3bottles.views.view import bp as bp_view  # noqa  # isort:skip

app.register_blueprint(bp_action)
app.register_blueprint(bp_admin)
app.register_blueprint(bp_api)
app.register_blueprint(bp_label)
app.register_blueprint(bp_main)
app.register_blueprint(bp_manage)
app.register_blueprint(bp_stats)
app.register_blueprint(bp_user)
app.register_blueprint(bp_view)
