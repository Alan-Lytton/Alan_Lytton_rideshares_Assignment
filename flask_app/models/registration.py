from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')

db = "ohana_rideshares"

class Registration:

    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def get_one_reg(cls, data):
        query = "select riders.id, riders.first_name, riders.last_name from riders WHERE id = %(rider_id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def register_rider(cls,data):
        query = "INSERT INTO riders (first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s) ;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_reg(rider):
        query = "SELECT * FROM riders WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, rider)
        is_valid = True
        if len(rider['fname']) < 2 or not rider['fname'].isalpha():
            flash('First Name must be more than 2 characters and only contain letters.', 'reg')
            is_valid = False
        if len(rider['lname']) < 2 or not rider['lname'].isalpha():
            flash('Last Name must be more than 2 characters and only contain letters.', 'reg')
        if not EMAIL_REGEX.match(rider['email']):
            flash('Invalid Email format.', 'reg')
            is_valid = False
        if len(results) > 0:
            flash('Email is already registered.', 'reg')
            print(results)
            is_valid = False
        if not PASSWORD_REGEX.match(rider['password']):
            flash('Password must be at least 8 characters long', 'reg')
            flash('Password must contain one upper case letter', 'reg')
            flash('Password must contain one lower case letter', 'reg')
            flash('Password must contain one number and one special character', 'reg')
            is_valid = False
        if not rider['password'] == rider['confirm_password']:
            flash('Provided passwords do not match.', 'reg')
            is_valid = False
        return is_valid