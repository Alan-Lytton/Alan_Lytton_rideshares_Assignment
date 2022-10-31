#this whole file can be changed depending on what we need to do with the data and how we want our OOP instances to appear.

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


db = "ohana_rideshares"  #add DB name inside quotes

class Detail:

    def __init__( self, data ):
        self.id = data['id']
        self.destination = data['destination']
        self.pick_up = data['pick_up']
        self.details = data['details']
        self.scheduled_at = data['scheduled_at']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.driver = None
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        # adjust the "FROM" target to be the required table
        query = "SELECT * FROM details;"
        # make sure to call the connectToMySQL function with the DB schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        details = []
        for detail in results:
            details.append( cls(detail) )
        return details

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM details WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        for row in results:
            one_detail = cls(row)
        return one_detail

    @classmethod
    def edit_one(cls,data):
        query = "UPDATE details SET pick_up = %(pickup)s, details = %(details)s WHERE id = %(details_id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def add_ride(cls,data):
        query = "INSERT INTO details (destination, pick_up, details, scheduled_at) VALUES (%(destination)s, %(pickup)s, %(details)s, %(pickup_date)s) ;"
        return connectToMySQL(db).query_db(query,data)
    

    @classmethod
    def get_details(cls,one_detail_info):
        results = cls(one_detail_info)
        results.driver = one_detail_info['driver']
        return results


    @classmethod
    def delete_details(cl,data):
        query = 'DELETE FROM details WHERE id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def validate_ride(ride):
        is_valid = True
        if len(ride['destination']) < 3:
            flash('Destination must be more than 3 characters long.')
            is_valid = False
        if len(ride['pickup']) < 3:
            flash('Pickup location must be more than 3 characters long.')
            is_valid = False
        if len(ride['details']) < 10:
            flash('Details must be more than 10 characters long')
        return is_valid

    @staticmethod
    def validate_edit(ride):
        is_valid = True
        if len(ride['pickup']) < 3:
            flash('Pickup location must be more than 3 characters long.')
            is_valid = False
        if len(ride['details']) < 10:
            flash('Details must be more than 10 characters long')
        return is_valid
