import qrcode
from sqlalchemy import or_
from base64 import b64encode
from cairosvg import svg2pdf
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO

from flask import render_template, Response, request, make_response

from .. import c3bottles, db

from ..model.drop_point import DropPoint


@c3bottles.route("/")
def index():
    return render_template("index.html")


@c3bottles.route("/faq")
def faq():
    return render_template("faq.html")


@c3bottles.route("/list")
def dp_list():
    return render_template("list.html",)


@c3bottles.route("/list.js")
def dp_list_js():
    resp = make_response(render_template(
        "js/list.js",
        all_dps_json=DropPoint.get_dps_json()
    ))
    resp.mimetype = "application/javascript"
    return resp


@c3bottles.route("/map")
def dp_map():
    return render_template("map.html")


@c3bottles.route("/map.js")
def dp_map_js():
    resp = make_response(render_template(
        "js/map.js",
        all_dps_json=DropPoint.get_dps_json()
    ))
    resp.mimetype = "application/javascript"
    return resp


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


@c3bottles.route("/view.js/<int:number>")
def dp_view_js(number):
    dp = DropPoint.get(number)
    resp = make_response(render_template(
        "js/view.js",
        all_dps_json=DropPoint.get_dps_json(),
        dp=dp
    ))
    resp.mimetype = "application/javascript"
    return resp


@c3bottles.route("/label/<int:number>.pdf")
def dp_label(number=None):
    dp = DropPoint.get(number)
    if dp:
        return Response(_pdf(number), mimetype="application/pdf")
    else:
        return render_template(
            "error.html",
            heading="Error!",
            text="Drop point not found.",
        )


@c3bottles.route("/label/all.pdf")
def dp_all_labels():
    output = PdfFileWriter()
    for dp in db.session.query.filter(or_(DropPoint.removed == None, ~DropPoint.removed)).all():
        output.addPage(PdfFileReader(BytesIO(_pdf(dp.number))).getPage(0))
    f = BytesIO()
    output.write(f)
    return Response(
        f.getvalue(),
        mimetype="application/pdf"
    )


def _pdf(number):
    img = qrcode.make(request.url_root + str(number))
    f = BytesIO()
    img.save(f)
    b64 = b64encode(f.getvalue()).decode("utf-8")
    
    return svg2pdf(render_template("empty34c3.svg", number=number, qr=b64))
