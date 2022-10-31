# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')

db = "ohana_rideshares"

class Login:

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
    def get_all(cls):
        # adjust the "FROM" target to be the required table
        query = "SELECT * FROM riders;"
        # make sure to call the connectToMySQL function with the DB schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        riders = []
        for rider in results:
            riders.append( cls(rider) )
        return riders

    @classmethod
    def get_one_login(cls, data):
        query = "select riders.id, riders.first_name, riders.last_name from riders WHERE email = %(email)s;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_login(rider):
        query = "SELECT * FROM riders WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, rider)
        is_valid = True
        if not EMAIL_REGEX.match(rider['email']):
            flash('Invalid Email format.', 'login')
            is_valid = False
        elif len(results) < 1:
            flash('Invalid Email/Password combination.', 'login')
            is_valid = False
        elif not bcrypt.check_password_hash(results[0]['password'], rider['password']):
            flash('Invalid Email/Password combination.', 'login')
            is_valid = False
        return is_valid
