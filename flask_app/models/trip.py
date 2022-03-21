from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Trip:
    db_name = 'travel-docs'

    def __init__(self, data):
        self.id = data['id']
        self.departing_country = data['departing_country']
        self.departing_country_code = data['departing_country_code']
        self.arriving_country = data['arriving_country']
        self.arriving_country_code = data['arriving_country_code']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Class method to save data to database
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO trips (departing_country, departing_country_code, arriving_country, arriving_country_code, user_id) VALUES (%(departing_country)s, %(departing_country_code)s, %(arriving_country)s, %(arriving_country_code)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Class method to get all objects in database
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM trips;'
        results = connectToMySQL(cls.db_name).query_db(query)
        all_trips = []
        for trip in results:
            all_trips.append(cls(trip))
        return all_trips

    # Class method to retrieve a database object by id
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM trips WHERE id=%(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(result[0])

    # Class method to update a database object
    @classmethod
    def update_trip(cls, data):
        query = 'UPDATE trips SET departing_country=%(departing_country)s, departing_country_code=%(departing_country_code)s, arriving_country=%(arriving_country)s, arriving_country_code=%(arriving_country_code)s, updated_at=NOW() WHERE id=%(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Class method to delete a database object
    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM trips WHERE id=%(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Static method to validate user input
    @staticmethod
    def validate_inputs(trip):
        is_valid = True
        if len(trip['departing_country']) < 1:
            flash('Please select a departing Country', 'trips')
            is_valid = False
        if len(trip['arriving_country']) < 1:
            flash('Please select a Country to travel to.', 'trips')
            is_valid = False
        return is_valid