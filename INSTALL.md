# System Requirements

In order to install c3bottles, you will need Python 3.5 or newer and the
following dependencies:

*   Flask
*   Flask-Babel
*   Flask-Bcrypt
*   Flask-SQLAlchemy
*   Flask-Login >= 0.3.0 (versions <0.3.0 will not work since a breaking
    change has been done in the API)
*   Flask-WTF
*   CairoSVG
*   PyPDF2
*   Python-QRCode
*   a WSGI-capable webserver (e.g. Apache)
*   some SQL server supported by SQLAlchemy
    (the author uses PostgreSQL but others should work, too)
*   ImageMagick, GDAL and the gdal2tiles.py script to generate the map tiles
*   the Node.js package manager (npm)
*   on Debian, Node.js is fucked up, so the legacy symlink is needed for npm
    etc. (node-legacy)

# Installation

1.  Clone the repository from Github:

        $ git clone https://github.com/c3bottles/c3bottles.git
        $ cd c3bottles

2.  Make sure all the dependencies are installed. The easiest way is to
    install them using `pip`:

        $ pip install -r requirements.txt

    If you are using Debian and the installation fails, you are probably
    missing `libpython3-dev` or `libffi-dev`.

    If you prefer a virtualenv, a Makefile has already been prepared for you,
    just type `make` to create it and install all dependencies.

3.  Fetch the frontend dependencies and build everything:

        $ npm install
        $ npm run build

4.  Create a configuriation file `config.py`. You will find a template for
    the configuration in the file `config.default.py`. Although c3bottles will
    work if no `config.py` with the required settings is present, is is
    recommended to set at least a SECRET_KEY and SQLALCHEMY_DATABASE_URI.

5.  Configure your database accordingly. The user for c3bottles needs full
    access to the database. If you use SQLite, the web server needs write
    access to the directory containing the `*.db` file and to the file itself.

6.  Initialize the database:

        $ ./manage.py initdb

7.  In order to use c3bottles, you need to create at least one admin user:

        $ ./manage.py user create

    Most user management tasks can be done via the command line interface.
    `./manage.py user --help` provides the details.

8.  For testing purposes, you can run c3bottles with the development web
    server included in Flask:

        $ ./manage.py run

    However, if you want to use c3bottles in a production environment, it is
    strongly advised to use a proper web server like lined out below.

9.  Configure your webserver accordingly to run the WSGI application.

    To use c3bottles with Apache, you need `mod_wsgi` for Python 3 (in Debian:
    `libapache2-mod-wsgi-py3) and in your virtual host, you need to add a
    configuration like this:

        WSGIScriptAlias / /path/to/c3bottles/wsgi.py
        WSGIApplicationGroup %{GLOBAL}
        Alias /static /path/to/c3bottles/static

    If your Python libraries are installed inside a virtualenv,
    `WSGIPythonHome` has to be set accordingly. Please keep in mind that this
    is a global setting of Apache.

    A sample uWSGI configuration file:

        [uwsgi]
        socket = /tmp/c3bottles.sock
        venv = /srv/c3bottles/venv
        chdir = /srv/c3bottles/
        wsgi-file = wsgi.py
        callable = c3bottles

# Map

There are two main ways of using the map: For an indoor event, you can use an
appropriate building plan as the base for the map tiles. For an outdoor event
it is useful to use a map source already present, namely OpenStreetMap. These
two ways are described below in the "Internal map" and "OpenStreetMap" sections,
respectively.

## Internal map

The internal map is the default when checking out c3bottles. To use the map you
first have to generate the map tiles. The normal build task already does that
with the map delivered with the package. If you replaced the map and just want
to regenerate the tiles using the defaults, you can do this with:

    $ npm run build:map

The standard source file for the map is `static/img/map.png`. For
tile generation, the image has to be a square whose height/width is a
power of 2. It is useful to resize and enlarge the image to the next power
of 2. This can be done with ImageMagick's `convert` utility as follows,
assuming that the image has a largest dimension between 8192 and 16384 and
a white background:

    $ cd /path/to/c3bottles/static/img
    $ convert map.png -background white -compose Copy -gravity center \
                      -resize 16384x16384 -extent 16384x16384 map_sq.png

An image size of 16384x16384 allows a maximum zoom level of 6 which is the
default in the JavaScript code of the map. If your image is larger or
smaller, the `maxZoom` setting in `static/js/map.js` has to be adapted
accordingly (i.e. to 5 for an 8192x8192 image).

Once you have a square source image with a power of 2 in size, you can
generate the tiles as follows:

    $ cd /path/to/c3bottles/static/img
    $ gdal_translate -of vrt map_sq.png map_sq.vrt
    $ gdal2tiles.py -w none -p raster map_sq.vrt tiles

`convert` may fail with newer ImageMagick versions on Debian due to memory
limits in ImageMagick. The issue can be solved by increasing the limits in
`/etc/ImageMagick-6/policy.xml`.

## OpenStreetMap

OpenStreetMap works out of the box once the USE\_OSM\_MAP configuration
parameter is set to True. Although, for it to be useful, you should set the
appropriate event location coordinates and a useful zoom level as default
view in `config.py`.
