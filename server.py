from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL # imports the database info
app = Flask(__name__)
app.secret_key = 'mqQPb4Mh!'
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

@app.route('/')
def route_to_index():
    return render_template('index.html')

@app.route('/process', methods=['post'])
def process_reg_form():

    # if there are errors:
    is_valid = True

    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        is_valid = False
        # display error message
        flash("Invalid email address!")
    if len(request.form['first_name']) < 1:
        is_valid = False
        # display error message
        flash("please enter first name")
    if len(request.form['last_name']) < 1:
        is_valid = False
        # display error message
        flash("please enter last name")
    if request.form['first_name'].replace(' ','',1).strip().isalpha() == False:
        print(request.form['first_name'].isalpha())
        is_valid = False
        # display error message
        flash("please use only letters in the first name text field")
    if request.form['last_name'].replace(' ','',1).strip().isalpha() == False:
        print(request.form['last_name'].isalpha())
        is_valid = False
        # display error message
        flash("please use only letters in the last name text field")
    if len(request.form['email']) < 1:
        is_valid = False
        # display error message
        flash("please enter an email")
    if len(request.form['password']) < 1:
        is_valid = False
        # display error message
        flash("please enter a password")
    if len(request.form['password']) < 5:
        is_valid = False
        # display error message
        flash("your password needs to be at least 5 characters in length")
    if request.form['password'] != request.form['confirm_password']:
        is_valid = False
        # display error message
        flash("confirm password and password need to be the same")

    if is_valid:
        print(request.form)
        mysql = connectToMySQL('basic_reg') # call the function, passing in the name of our db
        # QUERY: INSERT INTO registration (first_name, last_name, password, email) 
        # VALUES (first_name from db, last_name from db, password from db, email from db);
        query = 'insert into registration (first_name, last_name, password, email) values (%(first_name)s, %(last_name)s, %(password)s, %(email)s);'
        data ={
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'password': request.form['password'],
            'email': request.form['email']
        }
        print('response was true')
        flash("successfully added!")
        mysql.query_db(query, data)

    return  redirect('/')

if __name__ == "__main__":
    app.run(debug=True)