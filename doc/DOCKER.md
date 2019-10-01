# Install c3bottles using Docker

You probably want to adjust the `Dockerfile` and `docker-compose.yml` to your
specific requirements. However, the defaults should work just fine out of the
box for a testing or development environment:

1.  First you need to create a config.py file:

        cp config.default.py config.py

    Please set at least the `SECRET_KEY` and change the `SQLALCHEMY_DATABASE_URI`
    to your setup (for the default docker-compose setup, you should use
    `SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db/postgres"`)
    like in `config.default.py`.

2.  By default, docker-compose will download the image from Docker Hub. If you
    want to build your own image from source, please do:

        docker build -t c3bottles/c3bottles .

3.  Start the database using docker-compose:

        docker-compose up -d db

    A database web admin interface is available as well:

        docker-compose up -d db adminer

4.  Initialize the database:

        docker-compose run --rm app ./manage.py initdb

5.  Create a user:

        docker-compose run --rm app ./manage.py user create

6.  Start the web interface:

        docker-compose up -d app web

    The web interface will listen on port 8000 by default.

7.  If you are done with testing, simply stop and remove all the containers:

        docker-compose down
