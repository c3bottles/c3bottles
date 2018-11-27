from prometheus_client import Counter, Histogram, start_http_server, Gauge
from time import time

from flask import request

from .. import c3bottles
from .statistics import stats_obj


drop_point_count = Gauge(
    "c3bottles_drop_point_count", "c3bottles total nmumber of drop points"
)

drop_point_count.set_function(lambda: stats_obj.drop_point_count)

report_count = Gauge(
    "c3bottles_report_count", "c3bottles total number of reports"
)

report_count.set_function(lambda: stats_obj.report_count)

visit_count = Gauge(
    "c3bottles_visit_count", "c3bottles total number of visits"
)

visit_count.set_function(lambda: stats_obj.visit_count)

request_latency = Histogram(
    "c3bottles_request_latency_seconds", "c3bottles Request Latency", ["method", "endpoint"]
)

request_count = Counter(
    "c3bottles_request_count", "c3bottles Request Count", ["method", "endpoint", "http_status"]
)


def before_request():
    request.start_time = time()


def after_request(response):
    latency = time() - request.start_time
    request_latency.labels(request.method, request.endpoint).observe(latency)
    request_count.labels(request.method, request.endpoint, response.status_code).inc()
    return response


def monitor(app,
            address=c3bottles.config.get("PROMETHEUS_ADDRESS", "127.0.0.1"),
            port=c3bottles.config.get("PROMETHEUS_PORT", 9567)):
    app.before_request(before_request)
    app.after_request(after_request)
    start_http_server(port, address)
    print("Prometheus exporter started on http://{}:{}/".format(address, port))
