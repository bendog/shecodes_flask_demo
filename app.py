import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


##########
# config
##########


BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


##########
# our data
##########


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    description = db.Column(db.Text())



##########
# our pages
##########


@app.route('/')
def index():
    # # get the data
    all_projects= Project.query.all()
    # return to template
    return render_template(
        'index.html', # which template
        # all the variables for context go here
        title="my killer page",
        all_projects=all_projects
    )

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

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



##########
# code to run the server
##########


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)

