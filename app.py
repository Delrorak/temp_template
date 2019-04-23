from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy			# instead of mysqlconnection
from flask_migrate import Migrate			# this is new
from sqlalchemy.sql import func                         # ADDED THIS LINE FOR DEFAULT TIMESTAMP

app = Flask(__name__)
# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_authors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)

#secret key associated with our imported session and flash files
app.secret_key = 'mqQPb4Mh!'

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, # which is made by invoking the function Bcrypt with our app as an argument

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

@app.route('/')
def route_to_index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user_process():
    register_user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], email=request.form['email'], password=request.form['password'])
    db.session.add(register_user)
    db.session.commit()
    return redirect('/user_dashboard')

@app.route('/user_dashboard')
def author_index():
    return render_template('user_dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)