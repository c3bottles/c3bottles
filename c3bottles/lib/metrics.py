from time import time

from flask import request
from prometheus_client import Counter, Histogram, start_http_server, Gauge

from c3bottles import app
from c3bottles.model import drop_point
from c3bottles.model import report
from c3bottles.model import visit


drop_point_count = Gauge(
    "c3bottles_drop_point_count",
    "c3bottles count of drop points grouped by state and category",
    ["state", "category"],
)

report_count = Gauge(
    "c3bottles_report_count",
    "c3bottles count of reports grouped by state and category of drop point",
    ["state", "category"],
)

visit_count = Gauge(
    "c3bottles_visit_count",
    "c3bottles count of visits grouped by action and category of drop point",
    ["action", "category"],
)

request_latency = Histogram(
    "c3bottles_request_latency_seconds", "c3bottles Request Latency", ["method", "endpoint"],
)

request_count = Counter(
    "c3bottles_request_count", "c3bottles Request Count", ["method", "endpoint", "http_status"],
)


def before_request():
    request.start_time = time()


def after_request(response):
    latency = time() - request.start_time
    request_latency.labels(request.method, request.endpoint).observe(latency)
    request_count.labels(request.method, request.endpoint, response.status_code).inc()
    return response


def monitor(
    app,
    address=app.config.get("PROMETHEUS_ADDRESS", "127.0.0.1"),
    port=app.config.get("PROMETHEUS_PORT", 9567),
):
    for dp in drop_point.DropPoint.query.all():
        drop_point_count.labels(state=dp.last_state, category=dp.category.metrics_name).inc()
    for r in report.Report.query.all():
        report_count.labels(state=r.state, category=r.dp.category.metrics_name).inc()
    for v in visit.Visit.query.all():
        visit_count.labels(action=v.action, category=v.dp.category.metrics_name).inc()
    app.before_request(before_request)
    app.after_request(after_request)
    start_http_server(port, address)
    print("Prometheus exporter started on http://{}:{}/".format(address, port))
