# Install c3bottles using Docker

You probably want to adjust the `Dockerfile` and `docker-compose.yml` to your
specific requirements. However, the defaults should work just fin out of the
box for a testing or development environment:

1.  First you need to create your config.py file:

        cp config.default.py config.py

    Please set at least the `SECRET_KEY` and change the `SQLALCHEMY_DATABASE_URI`
    to your setup (for the default docker-compose setup, you should use
    `SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db/postgres"`).

2.  Start the database using docker-compose:

        docker-compose up -d db

    A database web admin interface is available as well:

        docker-compose up -d db adminer

3.  Initialize the database:

       docker-compose run --rm web /c3bottles/manage.py initdb

4.  Create a user:

        docker-compose run web /c3bottles/manage.py user create

5.  Start the web interface:

        docker-compose up -d web

    The web interface will listen on port 5000 by default.
