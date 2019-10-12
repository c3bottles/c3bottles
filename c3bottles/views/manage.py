from datetime import datetime

from flask import Blueprint, render_template, request, make_response, url_for, flash, redirect
from flask_babel import lazy_gettext

from c3bottles import db
from c3bottles.model.category import categories_sorted
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.location import Location
from c3bottles.views import needs_editing


bp = Blueprint("manage", __name__)


@bp.route("/create", methods=("GET", "POST"))
@bp.route("/create/<level>/<float:lat>/<float:lng>", methods=("GET", "POST"))
@needs_editing
def create(lat=None, lng=None, level=None, description=None, errors=None):
    if request.method == "POST":
        number = int(request.form.get("number"))
        category_id = int(request.form.get("category_id"))
        description = request.form.get("description")
        lat = float(request.form.get("lat"))
        lng = float(request.form.get("lng"))
        level = int(request.form.get("level"))
        try:
            dp = DropPoint(
                number=number, category_id=category_id, description=description,
                lat=lat, lng=lng, level=level
            )
            flash({
                "class": "success disappear",
                "text": lazy_gettext(
                    "Your %(category)s has been created successfully.", category=dp.category
                )
            })
            return redirect("{}#{}/{}/{}/3".format(url_for("view.map_"), level, lat, lng))
        except ValueError as e:
            errors = e.args
    else:
        number = DropPoint.get_next_free_number()

    if errors is not None:
        error_list = [v for d in errors for v in d.values()]
        error_fields = [k for d in errors for k in d.keys()]
    else:
        error_list = []
        error_fields = []

    return render_template(
        "manage/create.html",
        number=number,
        lat=lat,
        lng=lng,
        level=int(level),
        description=description,
        error_list=error_list,
        error_fields=error_fields,
        categories=categories_sorted(),
    )


@bp.route("/create.js/<level>/<float:lat>/<float:lng>")
def create_js(level, lat, lng):
    resp = make_response(render_template(
        "js/create.js",
        all_dps_json=DropPoint.get_dps_json(),
        level=int(level),
        lat=lat,
        lng=lng
    ))
    resp.mimetype = "application/javascript"
    return resp


@bp.route("/edit/<string:number>", methods=("GET", "POST"))
@bp.route("/edit")
@needs_editing
def edit(number=None, errors=None):
    dp = DropPoint.query.get_or_404(request.values.get("number", number))

    description_old = str(dp.description)
    lat_old = str(dp.lat)
    lng_old = str(dp.lng)
    level = dp.level

    if request.method == "POST":

        description = request.form.get("description")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        remove = request.form.get("remove")

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
            if remove == "yes":
                dp.removed = datetime.now()
            else:
                dp.removed = None
            db.session.commit()
            flash({
                "class": "success disappear",
                "text": lazy_gettext("Your changes have been saved successfully."),
            })
            return redirect("{}#{}/{}/{}/3".format(url_for("view.map_"), level, lat, lng))

        except ValueError as e:
            errors = e.args

    else:
        description = description_old
        lat = lat_old
        lng = lng_old

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
        "manage/edit.html",
        dp=dp,
        number=number,
        description=description,
        lat=lat_f,
        lng=lng_f,
        level=level,
        error_list=error_list,
        error_fields=error_fields
    )


@bp.route("/edit.js/<string:number>")
def edit_js(number):
    resp = make_response(render_template(
        "js/edit.js",
        all_dps_json=DropPoint.get_dps_json(),
        dp=DropPoint.query.get_or_404(number),
    ))
    resp.mimetype = "application/javascript"
    return resp
