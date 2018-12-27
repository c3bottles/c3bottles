import qrcode
from base64 import b64encode
from cairosvg import svg2pdf
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO
from stringcase import snakecase, lowercase

from flask import Blueprint, render_template, request, Response, abort

from c3bottles import app
from c3bottles.model.drop_point import DropPoint
from c3bottles.model.category import Category
from c3bottles.views import needs_visiting


bp = Blueprint("label", __name__)


@bp.route("/label/<int:number>.pdf")
@needs_visiting
def for_dp(number):
    dp = DropPoint.query.get(number)
    if (dp is None):
        return abort(404)
    return Response(_create_pdf(dp), mimetype="application/pdf")


@bp.route("/label/all.pdf")
@needs_visiting
def all_labels():
    output = PdfFileWriter()
    for dp in DropPoint.query.filter(DropPoint.removed == None).all():  # noqa
        output.addPage(PdfFileReader(BytesIO(_create_pdf(dp))).getPage(0))
    f = BytesIO()
    output.write(f)
    return Response(
        f.getvalue(),
        mimetype="application/pdf"
    )


@bp.route("/label/category/<int:number>.pdf")
@needs_visiting
def for_cat(number):
    cat = Category.get(number)
    if (cat is None):
        return abort(404)
    output = PdfFileWriter()
    for dp in DropPoint.query.filter(DropPoint.category_id == cat.category_id, DropPoint.removed == None).all():  # noqa
        output.addPage(PdfFileReader(BytesIO(_create_pdf(dp))).getPage(0))
    f = BytesIO()
    output.write(f)
    return Response(
        f.getvalue(),
        mimetype="application/pdf"
    )


def _create_pdf(dp: DropPoint):
    img = qrcode.make(request.url_root + str(dp.number))
    f = BytesIO()
    img.save(f)
    b64 = b64encode(f.getvalue()).decode("utf-8")
    label_style = app.config.get("LABEL_STYLE", "default")
    specific_label_style = label_style + "_" + snakecase(lowercase(dp.category.name))
    print(specific_label_style, label_style)
    try:
        return svg2pdf(render_template("label/{}.svg".format(specific_label_style), number=dp.number, qr=b64))  # noqa
    except:  # noqa
        return svg2pdf(render_template("label/{}.svg".format(label_style), number=dp.number, qr=b64))  # noqa
