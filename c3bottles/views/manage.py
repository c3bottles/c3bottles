from datetime import datetime

from flask import Blueprint, flash, make_response, redirect, render_template, request, url_for
from flask_babel import lazy_gettext

from c3bottles import db
from c3bottles.model.category import categories_sorted
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.location import Location
from c3bottles.views import needs_editing

bp = Blueprint("manage", __name__)


@bp.route("/create", methods=("GET", "POST"))
@bp.route("/create/<level>/<lat>/<lng>", methods=("GET", "POST"))
@needs_editing
def create(lat: str = None, lng: str = None, level: str = None):
    description = None
    errors = None
    if request.method == "POST":
        number = int(request.form.get("number"))
        category_id = int(request.form.get("category_id"))
        description = request.form.get("description")
        lat = float(request.form.get("lat"))
        lng = float(request.form.get("lng"))
        level = int(request.form.get("level"))
        try:
            dp = DropPoint(
                number=number,
                category_id=category_id,
                description=description,
                lat=lat,
                lng=lng,
                level=level,
            )
            flash(
                {
                    "class": "success disappear",
                    "text": lazy_gettext(
                        "Your %(category)s has been created successfully.", category=dp.category,
                    ),
                }
            )
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
        lat=float(lat),
        lng=float(lng),
        level=int(level),
        description=description,
        error_list=error_list,
        error_fields=error_fields,
        categories=categories_sorted(),
    )


@bp.route("/create.js/<level>/<lat>/<lng>")
def create_js(level: str, lat: str, lng: str):
    resp = make_response(
        render_template(
            "js/create.js",
            all_dps_json=DropPoint.get_dps_json(),
            level=int(level),
            lat=float(lat),
            lng=float(lng),
        )
    )
    resp.mimetype = "application/javascript"
    return resp


@bp.route("/edit/<int:number>", methods=("GET", "POST"))
@bp.route("/edit")
@needs_editing
def edit(number: int = None):
    dp = DropPoint.query.get_or_404(request.values.get("number", number))

    description_old = str(dp.description)
    lat_old = str(dp.lat)
    lng_old = str(dp.lng)
    level = dp.level

    errors = None

    if request.method == "POST":

        description = request.form.get("description")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        remove = request.form.get("remove")

        try:
            if description != description_old or lat != lat_old or lng != lng_old:
                Location(dp, description=description, lat=lat, lng=lng, level=level)
            if remove == "yes":
                dp.removed = datetime.now()
            else:
                dp.removed = None
            db.session.commit()
            flash(
                {
                    "class": "success disappear",
                    "text": lazy_gettext("Your changes have been saved successfully."),
                }
            )
            return redirect(f"{url_for('view.map_')}#{level}/{lat}/{lng}/3")

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
        error_fields=error_fields,
    )


@bp.route("/edit.js/<int:number>")
def edit_js(number: int):
    resp = make_response(
        render_template(
            "js/edit.js",
            all_dps_json=DropPoint.get_dps_json(),
            dp=DropPoint.query.get_or_404(number),
        )
    )
    resp.mimetype = "application/javascript"
    return resp
