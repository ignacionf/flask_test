# flask_test
## requirements

Docker, docker-compose, pipenv

## Initial

```
$ pipenv install
$ pipenv shell
$ python
>>> from crud import db, create_app, models
>>> db.create_all(app=create_app())

# Run
$ pipenv run flask run
```
## Start

```
$ docker-compose build web
$ docker-compose up -d db
$ docker-compose up db
```
