from datetime import datetime
from flask import render_template, request, g, abort, make_response, url_for
from flask_babel import lazy_gettext
from flask_login import login_required

from .. import c3bottles, db

from ..model.drop_point import DropPoint
from ..model.location import Location


@c3bottles.route("/edit/<string:number>", methods=("GET", "POST"))
@c3bottles.route("/edit")
@login_required
def edit_dp(number=None, errors=None):

    if not g.user.can_edit:
        abort(401)

    if number:
        dp = DropPoint.get(number)
    else:
        dp = DropPoint.get(request.values.get("number"))

    if not dp:
        return render_template(
            "error.html",
            heading=lazy_gettext("Error!"),
            text=lazy_gettext("Drop point not found.")
        )

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

        except ValueError as e:
            errors = e.args
        else:
            db.session.commit()
            return render_template(
                    "success.html",
                    text=lazy_gettext("Your changes have been saved successfully."),
                    back="{}#{}/{}/{}/3".format(url_for("dp_map"), level, lat, lng)
                )

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
        "edit_dp.html",
        number=number,
        description=description,
        lat=lat_f,
        lng=lng_f,
        level=level,
        error_list=error_list,
        error_fields=error_fields
    )


@c3bottles.route("/edit.js/<string:number>")
def edit_dp_js(number):
    resp = make_response(render_template(
        "js/edit_dp.js",
        all_dps_json=DropPoint.get_dps_json(),
        dp=DropPoint.get(number)
    ))
    resp.mimetype = "application/javascript"
    return resp
