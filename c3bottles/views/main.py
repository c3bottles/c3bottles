from flask import Blueprint, render_template


bp = Blueprint("main",  __name__)


@bp.route("/")
def index():
    return render_template("main/index.html")


@bp.route("/faq")
def faq():
    return render_template("main/faq.html")
