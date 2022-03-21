from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.trip import Trip

@app.route('/new/trip')
def new_trip():
    print('Got to new trip')
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('new_trip.html')

@app.route('/trip/<int:trip_id>')
def view_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': trip_id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('show_trip.html', trip=Trip.get_by_id(data), user=User.get_by_id(user_data))

@app.route('/edit/trip/<int:trip_id>')
def edit_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': trip_id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('edit_trip.html', edit=Trip.get_by_id(data), user=User.get_by_id(user_data))

@app.route('/destroy/trip/<int:trip_id>')
def destroy_trip(trip_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': trip_id
    }
    Trip.destroy(data)
    return redirect('/dashboard')

@app.route('/create/trip', methods=['POST'])
def create_trip():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Trip.validate_inputs(request.form):
        return redirect('/new/trip')
    data = {
        'departing_country': request.form['departing_country'],
        'departing_country_code' : request.form['departing_country_code'],
        'arriving_country': request.form['arriving_country'],
        'arriving_country_code' : request.form['arriving_country_code'],
        'user_id': session['user_id']
    }
    Trip.save(data)
    return redirect('/dashboard')

@app.route('/update/trip', methods=['POST'])
def update_trip():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': request.form['id'],
        'departing_country': request.form['departing_country'],
        'departing_country_code' : request.form['departing_country_code'],
        'arriving_country': request.form['arriving_country'],
        'arriving_country_code' : request.form['arriving_country_code'],
    }
    Trip.update_trip(data)
    return redirect('/dashboard')
