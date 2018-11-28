from flask import Blueprint, render_template


main = Blueprint("main",  __name__)


@main.route("/")
def index():
    return render_template("main/index.html")


@main.route("/faq")
def faq():
    return render_template("main/faq.html")
