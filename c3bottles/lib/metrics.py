from prometheus_client import Counter, Histogram, start_http_server, Gauge
from time import time

from flask import request

from . import stats_obj


drop_point_count = Gauge(
    "c3bottles_drop_point_count", "c3bottles dropoints"
)
def get_count():
    try:
        return stats_obj.drop_point_count
    except:
        return 0

drop_point_count.set_function(get_count)


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


def monitor(app, addr="0.0.0.0", port=9567):
    app.before_request(before_request)
    app.after_request(after_request)
    start_http_server(port, addr)
