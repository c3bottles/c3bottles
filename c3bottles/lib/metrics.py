from stringcase import snakecase, lowercase
from prometheus_client import Counter, Histogram, start_http_server, Gauge
from time import time
from flask import request

from c3bottles import app
from c3bottles.lib.statistics import stats_obj


overall_drop_point_count = Gauge(
    "c3bottles_overall_drop_point_count", "c3bottles total nmumber of drop points"
)

overall_drop_point_count.set_function(lambda: stats_obj.overall_drop_point_count)

for name, countFn in stats_obj.drop_points_by_category.items():
    category_gauge = Gauge("c3bottles_" + snakecase(lowercase(name)) + "_count",
                           "c3bottles number of " + name + " points")
    category_gauge.set_function(countFn)

for name, countFn in stats_obj.overall_drop_points_by_state_prometheus.items():
    dp_gauge = Gauge("c3bottles_overall_" + snakecase(lowercase(name)) +
                     "_count", "c3bottles number of overall " + name + " points")
    dp_gauge.set_function(countFn)

for cat_name, cat in stats_obj.drop_points_by_category_and_state.items():
    for state_name, countFn in cat.items():
        gauge = Gauge("c3bottles_" + snakecase(lowercase(cat_name)) + "_" +
                      snakecase(lowercase(state_name)), "c3bottles number of " + cat_name + " " + state_name)  # noqa
        gauge.set_function(countFn)

for cat_name, cat in stats_obj.reports_by_category_and_state.items():
    for state_name, countFn in cat.items():
        gauge = Gauge("c3bottles_reports_" + snakecase(lowercase(cat_name)) + "_" +
                      snakecase(lowercase(state_name)), "c3bottles number of reports " + cat_name + " " + state_name)  # noqa
        gauge.set_function(countFn)


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
            address=app.config.get("PROMETHEUS_ADDRESS", "127.0.0.1"),
            port=app.config.get("PROMETHEUS_PORT", 9567)):
    app.before_request(before_request)
    app.after_request(after_request)
    start_http_server(port, address)
    print("Prometheus exporter started on http://{}:{}/".format(address, port))
