from flask import render_template, redirect, request, flash, session
from config import db, bcrypt, re
from models import User, Quote
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def route_to_index():
    return render_template('index.html')

def register_new_user():
    validation_check = User.validate_user(request.form)
    if not validation_check: 
        return  redirect('/')  
    else:
        # create the hash 
        pw_hash = bcrypt.generate_password_hash(request.form['password'])  
        register_user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], email=request.form['email'], password=pw_hash)
        db.session.add(register_user)
        db.session.commit()
        user_id = register_user.id
        return redirect('/user_dashboard/'+ str(user_id))

def login_process():
    # if there are errors:
    is_valid = True

    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        is_valid = False
        # display error message
        flash("Invalid email address!")
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

    if is_valid:
        login_user = request.form["email"]
        filter_user = User.query.filter_by(email=login_user).scalar() is not None
        if filter_user == True:
            user = User.query.filter_by(email=login_user)
            user_password = request.form['password']
            if bcrypt.check_password_hash(user[0].password, request.form['password']):
            # if user[0].password == user_password:
                user_id = user[0].id
                return redirect('/user_dashboard/'+ str(user_id))
            else:
                flash("incorrect password")
                return redirect('/')
        else:
            flash("email not found")
            return redirect('/')
    flash("could not log you in")
    return redirect('/')

def user_dashboard(id):
    user_id = int(id)
    user_info = User.query.get(user_id)
    first_name = user_info.first_name
    last_name = user_info.last_name
    all_quotes = Quote.query.all()
    user_liked_quotes = user_info.quotes_this_user_liked
    
    return render_template('user_dashboard.html', user_id=user_id, first_name=first_name, last_name=last_name, all_quotes=all_quotes, user_liked_quotes=user_liked_quotes)

def logout():
    return render_template('/index.html')

def edit_account(id):
    user_id = id
    user_instance = User.query.get(user_id)
    first_name = user_instance.first_name 
    last_name = user_instance.last_name 
    email = user_instance.email
    return render_template('edit_account.html/', user_id = user_id, first_name = first_name, last_name = last_name, email = email)

def update_user(id):
    user_id = id
    validation_check = User.update_user(request.form)
    if not validation_check: 
        return redirect('/edit_account/' + user_id)
    else:
        user_instance_to_update = User.query.get(user_id)
        user_instance_to_update.first_name = request.form['first_name']
        user_instance_to_update.last_name = request.form['last_name']
        user_instance_to_update.email = request.form['email']
        db.session.commit()
    
def add_quote(id):
    user_id = id
    validation_check = Quote.validate_quote(request.form)
    if not validation_check: 
        return redirect('/user_dashboard/' + user_id)
    else:
        add_quote = Quote(author=request.form['author'], quote=request.form['quote'], user_id=user_id)
        db.session.add(add_quote)
        db.session.commit()
    return redirect('/user_dashboard/'+ user_id)

def user_posted_quotes(id, user_that_posted_id):
    user_id = id
    user_info = User.query.get(user_id)
    user_that_posted = user_that_posted_id
    print(user_that_posted)
    single_user_info = User.query.get(user_that_posted)
    first_name = single_user_info.first_name
    last_name = single_user_info.last_name
    all_single_user_quotes = single_user_info.user_quote
    return render_template('user.html', user_id=user_id, first_name=first_name, last_name=last_name, all_single_user_quotes=all_single_user_quotes)

def delete_quote(user_id, quote_id):
    print(user_id)
    print(quote_id)
    # db.session.query(Quote).filter_by(id=quote_id).delete() #This is how i deleted items
    db.session.query(Quote).filter_by(id=quote_id).delete()
    db.session.commit()
    return redirect('/user_dashboard/'+ user_id)

def likes(user_id, quote_id):
    
    existing_quote = Quote.query.get(quote_id)
    existing_user = User.query.get(user_id)
    existing_user.quotes_this_user_liked.append(existing_quote)
    db.session.commit()

    existing_user.quotes_this_user_liked
    print(existing_user.quotes_this_user_liked)

    return redirect('/user_dashboard/'+ user_id)