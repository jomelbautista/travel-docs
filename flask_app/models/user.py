from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name = 'travel-docs'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Class method to save data to database
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Class method to retrieve a database object by id
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id=%(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(result[0])

    # Class method to check if item exists in database
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email=%(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    # Static method to validate user input
    @staticmethod
    def validate_inputs(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email=%(email)s;'
        result = connectToMySQL(User.db_name).query_db(query, user)
        if len(result) >= 1:
            flash('Email is already in use.', 'registration')
            is_valid = False
        if len(user['first_name']) < 3:
            flash('First name must be at least 3 characters.', 'registration')
            is_valid = False
        if len(user['last_name']) < 3:
            flash('Last name must be at least 3 characters.', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address.', 'registration')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.', 'registration')
            is_valid = False
        if (user['password']) != (user['confirm_password']):
            flash('Passwords must match.', 'registration')
            is_valid = False
        return is_valid