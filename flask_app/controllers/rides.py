from flask import render_template, session, redirect, request, url_for
from flask_app.models import detail, trip, rider  #change this import line based on your extra .py file for generating OOP instances
from flask_app import app

@app.route('/rides/new')
def r_new_ride():
    if 'rider_id' not in session:
        return redirect('/')
    return render_template('new_ride.html')

@app.route('/rides/process', methods = ['POST'])
def f_process_rides():
    if not detail.Detail.validate_ride(request.form):
        return redirect('/rides/new')
    data1 = {
        'destination': request.form.get('destination'),
        'pickup': request.form.get('pickup'),
        'pickup_date': request.form.get('date_of_ride'),
        'details': request.form.get('details')
    }
    data2 = {
        'id': request.form.get('rider_id'),
        'detail_id': detail.Detail.add_ride(data1)
    }
    trip.Trip.add_trip(data2)
    return redirect('/dashboard')

@app.route('/rides/add/driver/<int:detail_id>/<int:driver_id>')
def add_new_driver(detail_id,driver_id):
    if 'rider_id' not in session:
        return redirect('/')
    trip.Trip.add_driver({'detail_id':detail_id, 'driver_id':driver_id})
    return redirect('/dashboard')

@app.route("/rides/edit/<int:id>")
def r_edit_trip(id):
    if 'rider_id' not in session:
        return redirect('/')
    return render_template('edit_trip.html', trip = detail.Detail.get_one({'id':id}))

@app.route('/rides/edit/process', methods = ['POST'])
def f_trip_edit_process():
    if not detail.Detail.validate_edit(request.form):
        return redirect(url_for('r_edit_trip', id = request.form['details_id']))
    detail.Detail.edit_one(request.form)
    return redirect("/dashboard")

@app.route('/rides/delete/<int:id>')
def delete_ride(id):
    if 'rider_id' not in session:
        return redirect('/')
    data = {'id':id}
    trip.Trip.delete_trip(data)
    detail.Detail.delete_details(data)
    return redirect('/dashboard')

@app.route('/rides/cancel/<int:id>')
def driver_cancel(id):
    if 'rider_id' not in session:
        return redirect('/')
    trip.Trip.cancel_driver({'id':id})
    return redirect('/dashboard')

@app.route('/rides/view/<int:id>')
def r_view_details(id):
    if 'rider_id' not in session:
        return redirect('/')
    riders = rider.Rider.get_one({'id':id})
    return render_template('view_trip.html', riders=riders)