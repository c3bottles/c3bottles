from flask import render_template, request, g, abort, make_response
from flask_login import login_required

from .. import c3bottles, db

from ..model.drop_point import DropPoint


@c3bottles.route("/create", methods=("GET", "POST"))
@c3bottles.route(
    "/create/<level>/<float:lat>/<float:lng>",
    methods=("GET", "POST")
)
@login_required
def create(type=None, lat=None, lng=None, level=None, description=None, errors=None):
    if not g.user.can_edit:
        abort(401)

    if request.method == "POST":
        number = request.form.get("number")
        description = request.form.get("description")
        lat = float(request.form.get("lat"))
        lng = float(request.form.get("lng"))
        level = int(request.form.get("level"))
        type = request.form.get("type") or "drop_point"
        try:
            DropPoint(
                type=type,
                number=number, description=description, lat=lat,
                lng=lng, level=level
            )
        except ValueError as e:
            errors = e.args
        else:
            db.session.commit()
            return render_template(
                "success.html",
                text="Your drop point has been created successfully."
            )
    else:
        number = DropPoint.get_next_free_number()

    if errors is not None:
        error_list = [v for d in errors for v in d.values()]
        error_fields = [k for d in errors for k in d.keys()]
    else:
        error_list = []
        error_fields = []

    return render_template(
        "create.html",
        type=type,
        number=number,
        lat=lat,
        lng=lng,
        level=int(level),
        description=description,
        error_list=error_list,
        error_fields=error_fields,
    )


@c3bottles.route("/create.js/<level>/<float:lat>/<float:lng>")
def create_dp_js(level, lat, lng):
    resp = make_response(render_template(
        "js/create_dp.js",
        all_dps_json=DropPoint.get_dps_json(type="drop_point"),
        level=int(level),
        lat=lat,
        lng=lng
    ))
    resp.mimetype = "application/javascript"
    return resp
