# System Requirements

In order to install c3bottles, you will need:

*   Flask (python-flask)

*   Flask-SQLAlchemy (python-flask-sqlalchemy)

*   a WSGI-capable webserver (e.g. Apache)

*   some SQL server supported by SQLAlchemy
    (the author uses PostgreSQL but others should work, too)

*   GDAL and the gdal2tiles.py script to generate the map tiles
    (gdal-bin and python-gdal)

# Installation

0.  Make sure all the dependencies are installed.
    On Debian using Apache, you can do:

        apt-get install python-flask python-flask-sqlalchemy \
                        libapache2-mod-wsgi gdal-bin python-gdal

1.  Copy the files into some directory readable by the web server.
    You can clone the repository from Github:

        git clone https://github.com/der-michik/c3bottles.git

2.  Create a configuriation file `config.py`. You will find a template for the
    configuration in the file `config.default.py`. c3bottles will not work if
    no config.py with the required settings is present.

3.  Configure your database accordingly. The user for c3bottles needs full
    access to the database. If you use SQLite, the web server needs write
    access to the directory containing the `*.db` file and the file itself.

4.  Initialize the database using the Python interpreter:

        $ cd /path/to/c3bottles
        $ python
        >>> from model import *
        >>> db.create_all()

5.  Configure your webserver accordingly to run the WSGI application. Apache
    needs something like this to run c3bottles as the document root of a host:
    
        WSGIScriptAlias / /path/to/c3bottles/c3bottles.wsgi
        Alias /static /path/to/c3bottles/static

6.  To be able to use the drop point map, generate the map tiles:

        $ cd /path/to/c3bottles/static/img
        $ gdal_translate -of vrt -expand rgba map.png map.vrt
        $ gdal2tiles.py -w none -p raster map.vrt tiles
