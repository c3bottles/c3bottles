from flask import render_template, request, redirect, url_for, g
from flask.ext.login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from werkzeug.routing import BuildError
from json import loads
from re import sub

from c3bottles import c3bottles, db
from model.drop_point import DropPoint
from model.location import Location
from model.capacity import Capacity
from model.user import User, load_user

@c3bottles.before_request
def before_request():
    g.user = current_user


@c3bottles.route("/")
def index():
    return render_template("index.html")


@c3bottles.route("/faq")
def faq():
    return render_template("faq.html")


@c3bottles.route("/numbers")
def statistics():
    return "TODO: Show some nice statistics"


@c3bottles.route("/list")
def dp_list():
    all_dps = []
    for dp in db.session.query(DropPoint).all():
        if not dp.removed:
            all_dps.append({
                "number": dp.number,
                "location": dp.get_current_location(),
                "reports_total": dp.get_total_report_count(),
                "reports_new": dp.get_new_report_count(),
                "priority": dp.get_priority(),
                "last_state": dp.get_last_state(),
                "crates": dp.get_current_crate_count(),
            })
    return render_template(
        "list.html",
        all_dps=sorted(all_dps, key=lambda k: k["priority"], reverse=True),
        all_dps_json=DropPoint.get_dps_json()
    )


@c3bottles.route("/map")
def dp_map():
    return render_template(
        "map.html",
        all_dps_json=DropPoint.get_dps_json()
    )


@c3bottles.route("/view/<int:number>")
@c3bottles.route("/view")
def dp_view(number=None):
    dp = DropPoint.get(number)
    if dp:
        history = dp.get_history()
        return render_template(
            "view.html",
            dp=dp,
            history=history
        )
    else:
        return render_template(
            "error.html",
            heading="Error!",
            text="Drop point not found.",
        )

@c3bottles.route("/report", methods=("GET", "POST"))
@c3bottles.route("/<int:number>")
def report(number=None):
    if number:
        dp = DropPoint.get(number)
    else:
        dp = DropPoint.get(request.values.get("number"))

    if not dp:
        return render_template(
            "error.html",
            heading="Error!",
            text="Drop point not found.",
        )

    state = request.values.get("state")

    if state:
        from model.report import Report
        try:
            Report(dp=dp, state=state)
        except ValueError as e:
            return render_template(
                "error.html",
                text="Errors occurred while processing your report:",
                errors=[v for d in e.message for v in d.values()]
            )
        else:
            db.session.commit()
            return render_template(
                "success.html",
                heading="Thank you!",
                text="Your report has been received successfully."
            )
    else:
        return render_template(
            "report.html",
            dp=dp
        )


@c3bottles.route("/visit/<int:dp_number>")
@login_required
def dp_visit(dp_number):
    if not g.user.can_visit():
        return unauthorized(None)
    return "TODO: Visit drop point " + str(dp_number)


@c3bottles.route("/create", methods=("GET", "POST"))
@c3bottles.route("/create/<string:lat>/<string:lng>", methods=("GET", "POST"))
@login_required
def create_dp(
        number=None, description=None, lat=None,
        lng=None, level=None, crates=None, errors=None,
        success=None, center_lat=None, center_lng=None
):

    if not g.user.can_edit():
        return unauthorized(None)

    if request.method == "POST":

        number = request.form.get("number")
        description = request.form.get("description")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        level = request.form.get("level")
        crates = request.form.get("crates")

        try:
            DropPoint(
                number=number, description=description, lat=lat,
                lng=lng, level=level, crates=crates
            )
        except ValueError as e:
            errors = e.message
        else:
            db.session.commit()
            if request.form.get("action") == "stay":
                center_lat = lat
                center_lng = lng
                number = None
                description = None
                lat = None
                lng = None
                level = None
                crates = None
                success = True
            else:
                return render_template(
                    "success.html",
                    text="Your drop point has been created successfully."
                )

    try:
        lat_f = float(lat)
        lng_f = float(lng)
    except (ValueError, TypeError):
        lat_f = None
        lng_f = None

    if errors is not None:
        error_list = [v for d in errors for v in d.values()]
        error_fields = [k for d in errors for k in d.keys()]
    else:
        error_list = []
        error_fields = []

    return render_template(
        "create_dp.html",
        all_dps_json=DropPoint.get_dps_json(),
        number=number,
        description=description,
        center_lat=center_lat,
        center_lng=center_lng,
        lat=lat_f,
        lng=lng_f,
        level=level,
        crates=crates,
        error_list=error_list,
        error_fields=error_fields,
        success=success
    )


@c3bottles.route("/edit/<string:number>", methods=("GET", "POST"))
@c3bottles.route("/edit")
@login_required
def edit_dp(
        number=None, description=None, lat=None,
        lng=None, level=None, crates=None, errors=None,
        success=None, center_lat=None, center_lng=None
):

    if not g.user.can_edit():
        return unauthorized(None)

    if number:
        dp = DropPoint.get(number)
    else:
        dp = DropPoint.get(request.values.get("number"))

    if not dp:
        return render_template(
            "error.html",
            heading="Error!",
            text="Drop point not found."
        )

    description_old = str(dp.get_current_location().description)
    lat_old = str(dp.get_current_location().lat)
    lng_old = str(dp.get_current_location().lng)
    level_old = str(dp.get_current_location().level)
    crates_old = str(dp.get_current_crate_count())

    if request.method == "POST":

        description = request.form.get("description")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        level = request.form.get("level")
        crates = request.form.get("crates")

        try:

            if description != description_old \
                    or lat != lat_old or lng != lng_old:
                Location(
                    dp,
                    description=description,
                    lat=lat,
                    lng=lng,
                    level=level
                )

            if crates != crates_old:
                Capacity(
                    dp,
                    crates=crates
                )

        except ValueError as e:
            errors = e.message
        else:
            db.session.commit()
            return render_template(
                    "success.html",
                    text="Your changes have been saved."
                )

    else:
        description = description_old
        lat = lat_old
        lng = lng_old
        level = level_old
        crates = crates_old

    try:
        lat_f = float(lat)
        lng_f = float(lng)
    except (ValueError, TypeError):
        lat_f = None
        lng_f = None

    if errors is not None:
        error_list = [v for d in errors for v in d.values()]
        error_fields = [k for d in errors for k in d.keys()]
    else:
        error_list = []
        error_fields = []

    return render_template(
        "edit_dp.html",
        all_dps_json=DropPoint.get_dps_json(),
        number=number,
        description=description,
        lat=lat_f,
        lng=lng_f,
        level=level,
        crates=crates,
        error_list=error_list,
        error_fields=error_fields
    )


@c3bottles.route("/login", methods=("POST", "GET"))
def login():
    try:
        back = redirect(
            url_for(
                request.form.get("return"),
                **loads(sub("( u)?'", "\"", request.form.get("args")))
            )
        )
    except BuildError:
        back = redirect(url_for("index"))
    username = request.form.get("username")
    password = request.form.get("password")
    if g.user and g.user.is_authenticated():
        return back
    user = User.get(username)
    if user and user.validate_password(password):
        login_user(user, remember=True)
        return back
    else:
        return render_template(
            "error.html",
            heading="Login failed!",
            text="Wrong user name or password."
        )


@c3bottles.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@c3bottles.errorhandler(401)
def unauthorized(e):
    return render_template(
        "error.html",
        heading="Unauthorized!",
        text="You do not have permission to view this page."
    ), 401


@c3bottles.errorhandler(404)
def not_found(e):
    return render_template(
        "error.html",
        heading="Not found",
        text="The requested URL was not found on the server."
    ), 404

# vim: set expandtab ts=4 sw=4:
