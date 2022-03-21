from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
# from flask_app.models.tv_show import TvShow

@app.route('/new')
def myTrips():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('new_tv_show.html')

@app.route('/show/<int:tv_show_id>')
def view_tv_show(tv_show_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': tv_show_id
    }
    user_data = {
        'id': session['user_id']
    }
    creator_id = TvShow.get_by_id
    return render_template('view_tv_show.html', tv_show=TvShow.get_by_id(data), user=User.get_by_id(user_data), poster=User.get_poster_by_id(data))

@app.route('/edit/<int:tv_show_id>')
def edit_tv_show(tv_show_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': tv_show_id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('edit_tv_show.html',edit=TvShow.get_by_id(data),user=User.get_by_id(user_data))

@app.route('/destroy/tv_show/<int:tv_show_id>')
def destroy_tv_show(tv_show_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': tv_show_id
    }
    TvShow.destroy(data)
    return redirect('/dashboard')

@app.route('/create/show', methods=['POST'])
def create_tv_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not TvShow.validate_inputs(request.form):
        return redirect('/new')
    # Hashing password upon registration using Bcrpyt
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'description': request.form['description'],
        'release_date': request.form['release_date'],
        'user_id': session['user_id'],
    }
    TvShow.save(data)
    return redirect('/dashboard')

@app.route('/update/tv_show', methods=['POST'])
def update_tv_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not TvShow.validate_inputs(request.form):
        tv_show_id = request.form['id']
        return redirect(f'/edit/{tv_show_id}')
    data = {
        'id': request.form['id'],
        'title': request.form['title'],
        'network': request.form['network'],
        'description': request.form['description'],
        'release_date': request.form['release_date'],
    }
    TvShow.update_tv_show(data)
    return redirect('/dashboard')