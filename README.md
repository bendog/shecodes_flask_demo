# Shecodes Flask Demo

Simplified demo of Flask

## install

    pipenv install

## run

    pipenv run flask run

## setup database

    pipenv run flask db init

## make migrations

    pipenv run flask db migrate

## apply migrations

    pipenv run flask db upgrade

## notable changes

1. use app.py as a name, as it avoids having to introduce the concept of environmental variables
1. avoid blueprints, as we don't need to introduce the concept of multi-app tennancy to beginners
1. using pipenv, as it will load a .env file and have the same commands on windows, mac and linux.
1. add a way to add data to the database via a website, this was more exciting than using a form somewhere else
1. decided to use just one python file, as it makes it easier to conceptualise what's going on