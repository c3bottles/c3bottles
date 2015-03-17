# System Requirements

In order to install c3bottles, you will need:

*   Flask (python-flask)

*   Flask-SQLAlchemy (python-flask-sqlalchemy)

*   a WSGI-capable webserver (e.g. Apache)

*   some SQL server supported by SQLALchemy (the author uses PostgreSQL but
    others may work, too)

# Installation

1.  Copy the files into some directory readable by the web server.
    You can clone the repository from Github:

        `git clone  https://github.com/Der-MichiK/c3bottles.git`

2.  Create a configuriation file `config.py`. You will find a template for the
    configuration in the file `config.default.py`. c3bottles will not work if
    no config.py with the required settings is present.

3.  Configure your database accordingly. The user for c3bottles needs full
    access to the database. If you use SQLite, the web server needs write
    access to the directory c3bottles lives in.

4.  Initialize the database using the Python interpreter:

        $ cd /path/to/c3bottles
        $ python
        >>> from model import *
        >>> db.create_all()

5.  Configure your webserver accordingly to run the WSGI application. Apache
    needs something like this to run c3bottles as the document root of a host:
    
        WSGIScriptAlias / /path/to/c3bottles/c3bottles.wsgi
        Alias /static /path/to/c3bottles/static
