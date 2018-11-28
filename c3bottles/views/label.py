import qrcode
from base64 import b64encode
from cairosvg import svg2pdf
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO

from flask import Blueprint, render_template, request, Response

from . import needs_visiting
from .. import c3bottles
from ..model.drop_point import DropPoint


label = Blueprint("label", __name__)


@label.route("/label/<int:number>.pdf")
@needs_visiting
def for_dp(number):
    DropPoint.query.get_or_404(number)
    return Response(_create_pdf(number), mimetype="application/pdf")


@label.route("/label/all.pdf")
@needs_visiting
def all_labels():
    output = PdfFileWriter()
    for dp in DropPoint.query.filter(DropPoint.removed == None).all():  # noqa
        output.addPage(PdfFileReader(BytesIO(_create_pdf(dp.number))).getPage(0))
    f = BytesIO()
    output.write(f)
    return Response(
        f.getvalue(),
        mimetype="application/pdf"
    )


def _create_pdf(number):
    img = qrcode.make(request.url_root + str(number))
    f = BytesIO()
    img.save(f)
    b64 = b64encode(f.getvalue()).decode("utf-8")
    label_style = c3bottles.config.get("LABEL_STYLE", "default")
    return svg2pdf(render_template("label/{}.svg".format(label_style), number=number, qr=b64))
