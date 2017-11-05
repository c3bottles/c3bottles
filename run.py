#!/usr/bin/env python3

from argparse import ArgumentParser
from werkzeug.contrib.profiler import ProfilerMiddleware

from c3bottles import c3bottles

parser = ArgumentParser()
parser.add_argument(
    "-p", "--profile", action="store_true",
    help="start development web server with profiling enabled"
)
args = parser.parse_args()

if args.profile:
    c3bottles.config["PROFILE"] = True
    c3bottles.wsgi_app = \
        ProfilerMiddleware(c3bottles.wsgi_app, restrictions=[30])

c3bottles.run(debug=True)

# vim: set expandtab ts=4 sw=4:
