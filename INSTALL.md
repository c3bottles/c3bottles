# System Requirements

In order to install c3bottles, you will need:

*   Flask (python-flask)

*   Flask-SQLAlchemy (python-flask-sqlalchemy)

*   a WSGI-capable webserver (e.g. Apache)

*   some SQL server supported by SQLAlchemy
    (the author uses PostgreSQL but others should work, too)

*   ImageMagick, GDAL and the gdal2tiles.py script to generate the map tiles
    (imagemagick, gdal-bin and python-gdal)

# Installation

0.  Make sure all the dependencies are installed.
    On Debian using Apache, you can do:

        $ apt-get install python-flask python-flask-sqlalchemy \
                          libapache2-mod-wsgi imagemagick gdal-bin python-gdal

1.  Copy the files into some directory readable by the web server.
    You can clone the repository from Github:

        $ git clone https://github.com/der-michik/c3bottles.git

2.  Create a configuriation file `config.py`. You will find a template for the
    configuration in the file `config.default.py`. c3bottles will not work if
    no config.py with the required settings is present.

3.  Configure your database accordingly. The user for c3bottles needs full
    access to the database. If you use SQLite, the web server needs write
    access to the directory containing the `*.db` file and the file itself.

4.  Initialize the database using the Python interpreter:

        $ cd /path/to/c3bottles
        $ python
        >>> from c3bottles import db
        >>> db.create_all()

5.  Configure your webserver accordingly to run the WSGI application. Apache
    needs something like this to run c3bottles as the document root of a host:

        WSGIScriptAlias / /path/to/c3bottles/c3bottles.wsgi
        Alias /static /path/to/c3bottles/static

6.  To be able to use the drop point map, you first have to generate the map
    tiles. The standard source file for the map is `static/img/map.png`. For
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
