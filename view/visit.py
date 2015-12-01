from flask import g, abort
from flask.ext.login import login_required

from controller import c3bottles

@c3bottles.route("/visit/<int:dp_number>")
@login_required
def visit(dp_number):
    if not g.user.can_visit:
        abort(401)
    return "TODO: Visit drop point " + str(dp_number)

# vim: set expandtab ts=4 sw=4:
