# Docker

create your config.py file

```cp config.default.py config.py```

set in the file at least the SECRET_KEY

and change the SQLALCHEMY_DATABASE_URI to your setup

(default docker-compose setup: ```SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db/postgres"```)



to start the database

```docker-compose up -d db```

to start the database + the database webadmin (development)

```docker-compose up -d db adminer```


initialize the database

```docker-compose run --rm web python3 /c3bottles/manage.py initdb```


to create a user

```docker-compose run web python3 /c3bottles/manage.py user create```


to start the c3bottles software

```docker-compose up -d web```