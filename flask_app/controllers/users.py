from flask import render_template, request, redirect, session, flash
from flask_app import app
# from flask_app.models.tv_show import TvShow
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def success():
    #if 'user_id' not in session:
        #return redirect('/logout')
    #data = {
        #'id': session['user_id']
    #}
    return render_template('dashboard.html')
    #return render_template('dashboard.html', user=User.get_by_id(data), tv_shows=TvShow.get_all())

@app.route('/my-trips')
def myTrips():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('my-trips', user=User.get_by_id(data), trips=TvShow.get_all())

# Logout
@app.route('/logout')
def logout():
    session.clear()
    print('Session Cleared')
    return redirect('/')

# POST routes
# Register a user
@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_inputs(request.form):
        return redirect('/')
    # Hashing password upon registration using Bcrpyt
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

# Clear session
@app.route('/destroy_session', methods=['POST'])
def reset_session():
    session.clear()
    print('Session Cleared')
    return redirect('/')

# Login user
@app.route('/user-login', methods=['POST'])
def userlogin():
    # Check if email provided exists in the database
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    # If user does not exist in the database
    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')