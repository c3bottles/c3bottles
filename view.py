from flask import render_template

from c3bottles import c3bottles, db

@c3bottles.route("/")
def index():
	return "Welcome to c3bottles!"

@c3bottles.route("/list")
def dp_list():
	from model import DropPoint
	all_dps = []
	for dp in db.session.query(DropPoint).order_by(DropPoint.number).all():
		all_dps.append({
			"number": dp.number,
			"location": dp.get_current_location(),
			"reports_total": dp.get_total_report_count(),
			"reports_new": dp.get_new_report_count()
			})
	return render_template("list.html", all_dps=all_dps)
