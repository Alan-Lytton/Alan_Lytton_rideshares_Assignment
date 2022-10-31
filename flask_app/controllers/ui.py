from flask import render_template, session, redirect
from flask_app.models import rider  #change this import line based on your extra .py file for generating OOP instances
from flask_app import app


@app.route("/dashboard")     # lines 6 through 11 can be changed depending on what we need server.py to do.
def index():
    # call the get all classmethod to get all riders
    if 'rider_id' not in session:
        return redirect('/')
    return render_template("dashboard.html", riders = rider.Rider.get_all())

