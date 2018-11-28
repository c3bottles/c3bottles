# Install c3bottles

## System Requirements

c3bottles is compatible with Python 3.5 or newer. Please see `requirements.txt`
for the Python dependencies. c3bottles depends on Gunicorn by default to make
creation of Docker images easier but can run behind any WSGI compatible
webserver, be it Gunicorn, uWSGI or Apache.

The state of all the drop points is maintained in a database, so you will need
a database that can is supported by SQLAlchemy, e.g. SQLite or PostgreSQL.
The author uses PostgreSQL, therefore Psycopg2 is already included in
`requirements.txt`.

To build the frontend dependencies, you will need Node.js and yarn or npm.

## Installation

1.  Clone the repository from Github:

        $ git clone https://github.com/c3bottles/c3bottles.git
        $ cd c3bottles

2.  Make sure all the dependencies are installed. The easiest way is to
    install them using `pip`:

        $ pip install -r requirements.txt

    If you are using Debian and the installation fails, you are probably
    missing `libpython3-dev` or `libffi-dev`.

    If you would like to use a virtualenv, a Makefile has already been
    prepared, just type `make` to create it and install all dependencies.

3.  Fetch the frontend dependencies and build everything:

        $ yarn
        $ yarn build

4.  Create a configuriation file `config.py`. You will find a template for
    the configuration in the file `config.default.py`. Although c3bottles will
    work if no `config.py` with the required settings is present, is is
    recommended to set at least `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI`.

5.  Configure your database accordingly. The user for c3bottles needs full
    access to the database. If you use SQLite, the web server needs write
    access to the directory containing the `*.db` file and to the file itself.

6.  Initialize the database:

        $ ./manage.py initdb

7.  In order to use c3bottles, you need to create at least one admin user:

        $ ./manage.py user create

    User management can be done via the admin web interface but most user
    management tasks are available via the command line interface as well.
    `./manage.py user --help` provides the details.

8.  For testing purposes, you can run c3bottles with the development web
    server included in Flask:

        $ ./manage.py run

    However, if you want to use c3bottles in a production environment, it is
    strongly advised to use a proper web server like lined out below.

## Web server configuration

c3bottles can be used behind any WSGI compatible web server. Some options and
configuration examples are described here. If you encounter problems with
modules not being found, please have a look in `wsgi.py` end uncomment the
modifications to the module search path.

### Gunicorn

c3bottles ships with Gunicorn by default. Simply run
`venv/bin/gunicorn --bind 0.0.0.0:5000 wsgi` or similar from the c3bottles
base directory to use the Gunicorn binary installed in the virtualenv.

### Apache

To use c3bottles with Apache, you need `mod_wsgi` for Python 3 (in Debian:
`libapache2-mod-wsgi-py3`) and in your virtual host, you need to add a
configuration like this:

    WSGIScriptAlias / /path/to/c3bottles/wsgi.py
    WSGIApplicationGroup %{GLOBAL}
    Alias /static /path/to/c3bottles/static

If your Python libraries are installed inside a virtualenv, `WSGIPythonHome`
has to be set accordingly. Please keep in mind that this is a global setting
of Apache.

### uWSGI

A sample uWSGI configuration file could look like this:

    [uwsgi]
    socket = /tmp/c3bottles.sock
    venv = /srv/c3bottles/venv
    chdir = /srv/c3bottles/
    wsgi-file = wsgi.py
    callable = c3bottles

## Prometheus

If you use Prometheus to collect service metrics, just uncomment
`PROMETHEUS_ENABLED` in the configuration. This will start a Prometheus
exporter together with the WSGI server. By defaults, metrics are available
at [http://127.0.0.1:9567/](http://127.0.0.1:9567/).

## Map

By default, c3bottles uses the map of [c3nav](https://c3nav.de/). However, it
is possible to configure any map source that is supported by Leaflet (e.g. Open
Streetmap) by adapting `js/map.js` accordingly.
