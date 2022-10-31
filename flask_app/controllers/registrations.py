from flask import redirect, request, session
from flask_app.models.registration import Registration  #change this import line based on your extra .py file for generating OOP instances
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

@app.route("/create_rider", methods = ['POST'])
def f_register():
    if not Registration.validate_reg(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password': pw_hash
    }
    data2 = {
        'rider_id': Registration.register_rider(data)
    }
    session['rider_id'] = Registration.get_one_reg(data2)
    return redirect('/dashboard')