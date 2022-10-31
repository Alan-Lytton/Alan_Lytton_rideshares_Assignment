#this whole file can be changed depending on what we need to do with the data and how we want our OOP instances to appear.

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import detail, trip


db = "ohana_rideshares"  #add DB name inside quotes

class Rider:

    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.details = []
        self.driver = None
    # Now we use class methods to query our database

    @classmethod
    def get_all(cls):
        # adjust the "FROM" target to be the required table
        query = "SELECT * FROM riders JOIN trips ON riders.id = trips.rider_id JOIN details ON trips.detail_id = details.id;"
        # make sure to call the connectToMySQL function with the DB schema you are targeting.
        results = connectToMySQL(db).query_db(query)
        riders = []
        for rider in results:
            # print(rider['driver_id'])
            one_rider = cls(rider)
            one_detail_info = {
                'id': rider['details.id'],
                'destination': rider['destination'],
                'pick_up': rider['pick_up'],
                'details': rider['details'],
                'scheduled_at': rider['scheduled_at'],
                'created_at': rider['created_at'],
                'updated_at': rider['updated_at'],
                'driver': rider['driver_id']
            }
            one_rider.driver = trip.Trip.get_trip_with_driver(one_detail_info)
            one_rider.details = detail.Detail.get_details(one_detail_info)
            riders.append(one_rider)
        return riders

    @classmethod
    def get_one(cls, data):
        # adjust the "FROM" target to be the required table
        query = """SELECT * FROM riders 
        JOIN trips ON riders.id = trips.rider_id 
        JOIN details ON trips.detail_id = details.id 
        WHERE details.id = %(id)s;"""
        # make sure to call the connectToMySQL function with the DB schema you are targeting.
        results = connectToMySQL(db).query_db(query,data)
        riders = []
        for rider in results:
            # print(rider['driver_id'])
            one_rider = cls(rider)
            one_detail_info = {
                'id': rider['details.id'],
                'destination': rider['destination'],
                'pick_up': rider['pick_up'],
                'details': rider['details'],
                'scheduled_at': rider['scheduled_at'],
                'created_at': rider['created_at'],
                'updated_at': rider['updated_at'],
                'driver': rider['driver_id']
            }
            one_rider.driver = trip.Trip.get_trip_with_driver(one_detail_info)
            one_rider.details = detail.Detail.get_details(one_detail_info)
            riders.append(one_rider)
        return riders
    
