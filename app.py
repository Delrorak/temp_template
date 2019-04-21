from flask import Flask, render_template, request, redirect, session, flash	
from flask_sqlalchemy import SQLAlchemy	# instead of mysqlconnection
from sqlalchemy.sql import func # ADDED THIS LINE FOR DEFAULT TIMESTAMP
from flask_migrate import Migrate # this is new
app = Flask(__name__) # configurations to tell our app about the database we'll be connecting to

#secret key associated with our imported session and flash files
app.secret_key = 'mqQPb4Mh!'

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_db_name_here.db' #rename to your chosen db name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)

#remember to 'flask db init' when you first set up this template
#remember to 'flask db migrate' when you change any class info
#remember to 'flask db upgrade' when you change any class info

class Dojo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dojo_name = db.Column(db.String(45))
    city = db.Column(db.String(45))
    state = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

class Ninja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dojo_id = db.Column(db.Integer, db.ForeignKey('dojo.id'), nullable = False)
    dojo = db.relationship('Dojo', foreign_keys=[dojo_id], backref="ninja_dojo", cascade="all")
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

@app.route('/')
def index():
    all_dojos = Dojo.query.all()
    all_ninjas = Ninja.query.all()
    return render_template('index.html', all_dojos = all_dojos, all_ninjas = all_ninjas)

@app.route('/add_dojo', methods=['POST'])
def add_dojo_process():
    new_instance_of_a_dojo = Dojo(dojo_name=request.form['dojo_name'], city=request.form['city'], state=request.form['state'])
    db.session.add(new_instance_of_a_dojo)
    db.session.commit()
    return redirect('/')

@app.route('/add_ninja', methods=['POST'])
def add_ninja_process():
    new_instance_of_a_ninja = Ninja(first_name=request.form['first_name'], last_name=request.form['last_name'], dojo_id=request.form['dojo_id'])
    db.session.add(new_instance_of_a_ninja)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
