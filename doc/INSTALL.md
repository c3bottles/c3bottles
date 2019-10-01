# Install c3bottles

## System Requirements

c3bottles is compatible with Python 3.5 or newer. Please see `requirements.txt`
for the Python dependencies. c3bottles can run behind any WSGI compatible
webserver, be it Gunicorn, uWSGI or Apache. The usual deployment as shown in
the `Dockerfile` and `docker-compose.yml` uses Gunicorn behind an nginx reverse
proxy.

The state of all the drop points is maintained in a database, so you will need
a database that is supported by SQLAlchemy, e.g. SQLite or PostgreSQL. The
author uses PostgreSQL, therefore Psycopg2 is already included in
`requirements.txt` but most databases that are supported by SQLAlchemy should
work without any problem.

To build the frontend dependencies, you will need Node.js and yarn.

## Installation

1.  Clone the repository from Github:

        git clone https://github.com/c3bottles/c3bottles.git
        cd c3bottles

2.  Make sure all the dependencies are installed. The easiest way is to
    install them using `pip`:

        pip install -r requirements.txt

    If the installation fails, you are probably missing `libpython3-dev`,
    `libpq-dev` or `libffi-dev`.

    If you would like to use a virtualenv, a Makefile has already been
    prepared, just type `make` to create it and install all dependencies.

3.  Fetch the frontend dependencies and build everything:

        yarn
        yarn build

4.  Create a configuriation file `config.py`. You will find a template for
    the configuration in the file `config.default.py`. Although c3bottles will
    work if no `config.py` with the required settings is present, it is
    recommended to set at least `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI`.

5.  Configure your database accordingly. The user for c3bottles needs full
    access to the database. If you use SQLite, the web server needs write
    access to the directory containing the `*.db` file and to the file itself.

6.  Initialize the database:

        ./manage.py initdb

7.  In order to use c3bottles, you need to create at least one admin user:

        ./manage.py user create

    User management can be done via the admin web interface but most user
    management tasks are available via the command line interface as well.
    `./manage.py user --help` provides the details.

8.  For testing purposes, you can run c3bottles with the development web
    server included in Flask:

        ./manage.py run

    However, if you want to use c3bottles in a production environment, it is
    strongly advised to use a proper web server like lined out below.

## Web server configuration

c3bottles can be used behind any WSGI compatible web server. Some options and
configuration examples are described here. If you encounter problems with
modules not being found, please have a look in `wsgi.py` end uncomment the
modifications to the module search path.

### Gunicorn (+nginx)

Install Gunicorn and then simply run `gunicorn --bind 127.0.0.1:5000 wsgi` or
similar from the c3bottles base directory. It is recommended to use nginx
as a reverse proxy together with Gunicorn handling the dynamic part whereas
nginx serves the static content. This can be achieved with an nginx server
configuration like this:

    server {
      root /path/to/c3bottles;
      location / {
        try_files $uri @proxy_to_app;
      }
      location @proxy_to_app {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:5000;
      }
    }

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

c3bottles is only useful if a map has been configured. To do this, you have to
set a `MAP_SOURCE` in `config.py`. The different sources available are
implemented in `c3bottles/config/map.py`. If you do not want to redefine one of
the sources directly in the Python code, you can override single parameters of
the current source in `config.py`.

In general, c3bottles is able to use any map that can be configured as a layer
in [Leaflet](https://leafletjs.com/). Please see [MAP.md](MAP.md) for all
documentation regarding map sources, their parameters and how to define your
own.
