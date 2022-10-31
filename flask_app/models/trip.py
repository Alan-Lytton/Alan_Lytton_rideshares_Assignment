#this whole file can be changed depending on what we need to do with the data and how we want our OOP instances to appear.

# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import rider



db = "ohana_rideshares"  #add DB name inside quotes

class Trip:

    def __init__(self, data ):
        self.id = data['id']
        self.rider_id = data['rider_id']
        self.detail_id = data['detail_id']
        self.driver_id = data['driver_id']
        self.driver = None
    # Now we use class methods to query our database

    @classmethod
    def add_trip(cls,data):
        query = 'INSERT INTO trips (rider_id, detail_id) VALUES (%(id)s, %(detail_id)s);'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete_trip(cls,data):
        query = 'DELETE FROM trips WHERE detail_id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def cancel_driver(cls,data):
        query = 'UPDATE trips SET driver_id = null WHERE detail_id = %(id)s;'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_trip_with_driver(cls,data):
        query = "SELECT * FROM trips JOIN riders ON trips.driver_id = riders.id WHERE driver_id = %(driver)s;"
        results = connectToMySQL(db).query_db(query,data)
        all_trips = []
        for trip in results:
            one_trip = cls(trip)
            one_trip_user_info = {
                'id': trip['riders.id'],
                'first_name': trip['first_name'],
                'last_name': trip['last_name'],
                'email': trip['email'],
                'password': None,
                'created_at': trip['created_at'],
                'updated_at': trip['updated_at']
            }
            one_driver = rider.Rider(one_trip_user_info)
            one_trip.driver = one_driver
            print(one_trip.driver)
            all_trips.append(one_trip)
        return all_trips

    @classmethod
    def add_driver(cls,data):
        query = "UPDATE trips SET driver_id = %(driver_id)s WHERE detail_id = %(detail_id)s;"
        return connectToMySQL(db).query_db(query, data)
