# Shecodes Flask Demo

Simplified demo of Flask

You'll need to install pipenv to create your virtual environment, to enable the .env file for the environment variable settings, and also to run the commands to run flask.

installing pipenv is as easy as
- `sudo pip3 install pipenv` (on mac)
- `pip install pipenv` (on windows)

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


## process of creating app.py

### **stage one:** show something

install flask

    $ pipenv --three
    $ pipenv install flask

create the environment file

`.env`
```shell
FLASK_ENV=development
```

create the app

` app.py`
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
```

run flask

    $ pipenv run flask run

### **stage two:** show something pretty

copy in templates directory and files

edit `app.py`
```python
from flask import Flask, render_templates

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
```

### **stage three:** show more things

edit `app.py`
```python
from flask import Flask, render_templates

app = Flask(__name__)

@app.route('/')
def index():
    # return to template
    return render_template(
        'index.html', # which template
        # all the variables for context go here
        projects=[
            {'name': 'day 1', 'description': 'html/css'},
            {'name': 'day 2', 'description': 'python!'},
            {'name': 'day 3', 'description': 'flask'},
        ],
    )

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
```

talk about how templates work:

- context values
- loops
- include
- extend

### **stage four:** create the database

there's a lot of bits that need to be added here, most of this can be copy paste, but it's good to walk through.

#### add packages with pipenv

    $ pipenv install flask-sqlalchemy
    $ pipenv install flask-migrate

next we edit `app.py`, i'm going to do this in stages starting from the top.

#### setting up our flask database

```python
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


##########
# config
##########


BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

...
```

We have to add a lot of config to our project to get the database working.
- we need to import SQLAlchemy and Migrate
- we need to configure where the database will be found
- then we need to bind the database to our flask app

#### defining our database model

I've chosen to do this in the same file, rather than creating a models.py file, because, we're aiming for absolute beginners, multiple files is just difficult to make sure everyone is editing the same file.

```python

...
# after migrate

# our project table
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    description = db.Column(db.Text())


# before app.route('/')
...
```

this is our table for our projects.

#### reading from the database model

this is pretty simple, we just make our 

```python
...
@app.route('/')
def index():
    # # get the data
    all_projects= Project.query.all()
    # return to template
    return render_template(
        'index.html', # which template
        # all the variables for context go here
        all_projects=all_projects
    )
...
```

#### initialise, migrate and upgrade the database

    $ pipenv run flask db init
    Creating directory /Users/bendog/dev/shecodes_flask_demo/migrations ...  done
    Creating directory /Users/bendog/dev/shecodes_flask_demo/migrations/versions ...  done
    Generating /Users/bendog/dev/shecodes_flask_demo/migrations/script.py.mako ...  done
    Generating /Users/bendog/dev/shecodes_flask_demo/migrations/env.py ...  done
    Generating /Users/bendog/dev/shecodes_flask_demo/migrations/README ...  done
    Generating /Users/bendog/dev/shecodes_flask_demo/migrations/alembic.ini ...  done
    Please edit configuration/connection/logging settings in '/Users/bendog/dev/shecodes_flask_demo/migrations/alembic.ini' before proceeding.

    $ pipenv run flask db migrate
    INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.autogenerate.compare] Detected added table 'project'
    INFO  [alembic.autogenerate.compare] Detected added index 'ix_project_name' on '['name']'
    Generating /Users/bendog/dev/shecodes_flask_demo/migrations/versions/1994ef3acb05_.py ...  done

    $ pipenv run flask db upgrade
    INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> 1994ef3acb05, empty message

    $ pipenv run flask run

after running these commands, flask should be running again and happy, however there's no data in the database, so lets add a way to add data.

### **stage five:**  adding data to the database.

create a new html template

`update.html`
```html
{% extends 'base.html' %}

{% block heading %}
    <h1>Update Project</h1>
{% endblock %}

{% block content %}
<form  method="POST" action="">
    <input type="text" name="name" placeholder="Project name">
    <textarea name="description" placeholder="Project description"></textarea>
    <button type="submit">Send Message</button>
</form>
{% endblock %}
```

update `nav.html`
```html
<nav>
    <a href="{{ url_for('index') }}">Home</a>
    <a href="{{ url_for('about') }}">About</a>
    <a href="{{ url_for('contact') }}">Contact</a>
    <a href="{{ url_for('update') }}">Update</a>
</nav>
```

now add a new route to `app.py`
```python
...

@app.route('/update', methods=['GET', 'POST'])
def update():
    # get the data from the form
    if request.form:
        data = request.form
        # get the name
        name = data['name']
        print('name:', name)
        # get the description
        description = data['description']
        print('description:', description)

        # put the data in the database
        new_project = Project(name=name, description=description)
        db.session.add(new_project)
        db.session.commit()
        
        # redirect to home
        return redirect(url_for("index"), code=303)

    return render_template('update.html')

...
```

now our students can use a form to add new content to their index page, they get to see the joy of taking in data and seeing it change their page before their eyes!
