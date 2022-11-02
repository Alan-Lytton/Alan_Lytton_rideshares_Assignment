from flask import render_template, redirect, request, session
from flask_app.models.login import Login  #change this import line based on your extra .py file for generating OOP instances
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

@app.route("/")     # lines 6 through 11 can be changed depending on what we need controller to do.
def home():
    return render_template("log_reg.html")

@app.route('/destroy-session')
def destroy():
    session.clear()
    return redirect('/')

@app.route('/login', methods = ['POST'])
def f_login():
    if not Login.validate_login(request.form):
        session['email2'] = request.form['email']
        return redirect('/')
    session.clear()
    data = {
        'email': request.form['email']
    }
    rider_id = Login.get_one_login(data)
    session['rider_id'] = rider_id
    return redirect('/dashboard')