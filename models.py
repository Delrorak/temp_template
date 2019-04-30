from flask import flash
from sqlalchemy.sql import func
from config import db, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

user_like_table = db.Table('likes_user', 
              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), 
              db.Column('quote_id', db.Integer, db.ForeignKey('quote.id'), primary_key=True),)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(45))
    quote = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref="user_quote", cascade="all")
    user_who_liked_this_quote = db.relationship('User', secondary=user_like_table)
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_quote(cls, quote_data):
        is_valid = True
        if len(quote_data['author']) < 3:
            is_valid = False
            # display error message
            flash("please enter Author name that is longer than 3 characters")
        if len(quote_data['quote']) < 10:
            is_valid = False
            # display error message
            flash("The quote needs to be larger than 10 characters")
        return is_valid

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(60))
    quotes_this_user_liked = db.relationship('Quote', secondary=user_like_table)
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_user(cls, user_data):
        is_valid = True
        if not EMAIL_REGEX.match(user_data['email']):    # test whether a field matches the pattern
            is_valid = False
            # display error message
            flash("Invalid email address!")
        if len(user_data['first_name']) < 1:
            is_valid = False
            # display error message
            flash("please enter first name")
        if len(user_data['last_name']) < 1:
            is_valid = False
            # display error message
            flash("please enter last name")
        if user_data['first_name'].replace(' ','',1).strip().isalpha() == False:
            is_valid = False
            # display error message
            flash("please use only letters in the first name text field")
        if user_data['last_name'].replace(' ','',1).strip().isalpha() == False:
            is_valid = False
            # display error message
            flash("please use only letters in the last name text field")
        if len(user_data['email']) < 1:
            is_valid = False
            # display error message
            flash("please enter an email")
        if len(user_data['password']) < 1:
            is_valid = False
            # display error message
            flash("please enter a password")
        if len(user_data['password']) < 5:
            is_valid = False
            # display error message
            flash("your password needs to be at least 5 characters in length")
        if user_data['password'] != user_data['confirm_password']:
            is_valid = False
            # display error message
            flash("confirm password and password need to be the same")
        return is_valid

    @classmethod
    def update_user(cls, user_data):
        is_valid = True
        if not EMAIL_REGEX.match(user_data['email']):    # test whether a field matches the pattern
            is_valid = False
            # display error message
            flash("Invalid email address!")
        if len(user_data['first_name']) < 1:
            is_valid = False
            # display error message
            flash("please enter first name")
        if len(user_data['last_name']) < 1:
            is_valid = False
            # display error message
            flash("please enter last name")
        if user_data['first_name'].replace(' ','',1).strip().isalpha() == False:
            is_valid = False
            # display error message
            flash("please use only letters in the first name text field")
        if user_data['last_name'].replace(' ','',1).strip().isalpha() == False:
            is_valid = False
            # display error message
            flash("please use only letters in the last name text field")
        if len(user_data['email']) < 1:
            is_valid = False
            # display error message
            flash("please enter an email")
        return is_valid

