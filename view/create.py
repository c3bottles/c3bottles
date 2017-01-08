from flask import render_template, request, g, abort
from flask_login import login_required

from controller import c3bottles, db
from model.drop_point import DropPoint


@c3bottles.route("/create", methods=("GET", "POST"))
@c3bottles.route("/create/<string:lat>/<string:lng>", methods=("GET", "POST"))
@login_required
def create_dp(
        number=None, description=None, lat=None,
        lng=None, level=None, errors=None,
        success=None, center_lat=None, center_lng=None
):

    if not g.user.can_edit:
        abort(401)

    if request.method == "POST":

        number = request.form.get("number")
        description = request.form.get("description")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        level = request.form.get("level")

        try:
            DropPoint(
                number=number, description=description, lat=lat,
                lng=lng, level=level
            )
        except ValueError as e:
            errors = e.args
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
        error_list=error_list,
        error_fields=error_fields,
        success=success
    )

# vim: set expandtab ts=4 sw=4:
