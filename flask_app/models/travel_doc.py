from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class TvShow:
    db_name = 'travel-docs'

    def __init__(self, data):
        self.id = data['id']
        self.travel_doc = data['travel_doc']
        self.source = data['source']
        self.owned = data['owned']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Class method to save data to database
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO docs (title, network, description, release_date, user_id) VALUES (%(title)s, %(network)s, %(description)s, %(release_date)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Class method to get all objects in database
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM tv_shows;'
        results = connectToMySQL(cls.db_name).query_db(query)
        all_tv_shows = []
        for tv_show in results:
            all_tv_shows.append(cls(tv_show))
        return all_tv_shows

    # Class method to retrieve a database object by id
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM tv_shows WHERE id=%(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(result[0])

    # Class method to update a database object
    @classmethod
    def update_tv_show(cls, data):
        query = 'UPDATE tv_shows SET title=%(title)s, network=%(network)s, description=%(description)s, release_date=%(release_date)s, updated_at=NOW() WHERE id=%(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Class method to delete a database object
    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM tv_shows WHERE id=%(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Static method to validate user input
    @staticmethod
    def validate_inputs(tv_show):
        is_valid = True
        if len(tv_show['title']) < 3:
            flash('Title must be at least 3 characters long.', 'tv_show')
            is_valid = False
        if len(tv_show['network']) < 3:
            flash('Network must be at least 3 characters long.', 'tv_show')
            is_valid = False
        if tv_show['release_date'] == '':
            flash('Enter the release date.', 'tv_show')
            is_valid = False
        if len(tv_show['description']) < 3:
            flash('Description must be at least 3 characters long.', 'tv_show')
            is_valid = False
        return is_valid