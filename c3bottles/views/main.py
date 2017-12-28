import qrcode
from sqlalchemy import or_, and_
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


@c3bottles.route("/bottle/list")
def dp_list_bottle():
    return render_template("list.html",js_name="dp_list_js_bottle",title_name="Bottle Drop Points",maptype="dp_map_bottle",dp_type="drop_point")

@c3bottles.route("/trash/list")
def dp_list_trash():
    return render_template("list.html",js_name="dp_list_js_trash",title_name="Trashcans",maptype="dp_map_trash",dp_type="trashcan")


@c3bottles.route("/bottle/list.js")
def dp_list_js_bottle():
    resp = make_response(render_template(
        "js/list.js",
        all_dps_json=DropPoint.get_dps_json(type="drop_point")
    ))
    resp.mimetype = "application/javascript"
    return resp

@c3bottles.route("/tash/list.js")
def dp_list_js_trash():
    resp = make_response(render_template(
        "js/list.js",
        all_dps_json=DropPoint.get_dps_json(type="trashcan")
    ))
    resp.mimetype = "application/javascript"
    return resp


@c3bottles.route("/bottle/map")
def dp_map_bottle():
    return render_template("map.html",js_name="dp_map_js_bottle",dp_type="drop_point")

@c3bottles.route("/trash/map")
def dp_map_trash():
    return render_template("map.html",js_name="dp_map_js_trash",db_type="trashcan")


@c3bottles.route("/bottle/map.js")
def dp_map_js_bottle():
    resp = make_response(render_template(
        "js/map.js",
        all_dps_json=DropPoint.get_dps_json(type="drop_point")
    ))
    resp.mimetype = "application/javascript"
    return resp


@c3bottles.route("/trash/map.js")
def dp_map_js_trash():
    resp = make_response(render_template(
        "js/map.js",
        all_dps_json=DropPoint.get_dps_json(type="trashcan")
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
            history=history,
            typename=dp.get_typename()
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
        return Response(_pdf(number, dp.type), mimetype="application/pdf")
    else:
        return render_template(
            "error.html",
            heading="Error!",
            text="Drop point not found.",
        )


@c3bottles.route("/bottle/label/all.pdf")
def dp_all_labels_bottle():
    output = PdfFileWriter()
    for dp in db.session.query(DropPoint).filter(and_(or_(DropPoint.removed == None, ~DropPoint.removed), DropPoint.type == 'drop_point')).all():
        output.addPage(PdfFileReader(BytesIO(_pdf(dp.number, dp.type))).getPage(0))
    f = BytesIO()
    output.write(f)
    return Response(
        f.getvalue(),
        mimetype="application/pdf"
    )

@c3bottles.route("/label/all.pdf")
def dp_all_labels():
    output = PdfFileWriter()
    for dp in db.session.query(DropPoint).filter(or_(DropPoint.removed == None, ~DropPoint.removed)).all():
        output.addPage(PdfFileReader(BytesIO(_pdf(dp.number, dp.type))).getPage(0))
    f = BytesIO()
    output.write(f)
    return Response(
        f.getvalue(),
        mimetype="application/pdf"
    )

@c3bottles.route("/trash/label/all.pdf")
def dp_all_labels_trash():
    output = PdfFileWriter()
    for dp in db.session.query(DropPoint).filter(and_(or_(DropPoint.removed == None, ~DropPoint.removed), DropPoint.type == 'trashcan')).all():
        output.addPage(PdfFileReader(BytesIO(_pdf(dp.number, dp.type))).getPage(0))
    f = BytesIO()
    output.write(f)
    return Response(
        f.getvalue(),
        mimetype="application/pdf"
    )




def _pdf(number, type):
    img = qrcode.make(request.url_root + str(number))
    f = BytesIO()
    img.save(f)
    b64 = b64encode(f.getvalue()).decode("utf-8")

    if (type == 'drop_point'):
        return svg2pdf(render_template("empty34c3.svg", number=number, qr=b64))
    else:
        return svg2pdf(render_template("empty34c3_trash.svg", number=number, qr=b64))

