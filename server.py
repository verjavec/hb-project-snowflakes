""" Server for Snowflake patterns. """

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db
import crud
import os
import sys

import cloudinary
import cloudinary.uploader
import cloudinary.api

from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ.get('api_key')
API_SECRET = os.environ.get('api_secret')


@app.route('/')
def homepage():
    """ View homepage """

    return render_template('homepage.html')

@app.route('/users')
def all_users():
    """ View all users """

    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """ Show details for a particular user """

    user = crud.get_user_by_id(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users', methods=['POST'])
def register_user():
    """ Create a new user """

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    
    if user:
        flash('Account with that email already exists. Try again.')
    else:
        crud.create_user(email, name, password)
        flash('Account created! Please log in.')

    return redirect('/')

@app.route('/', methods=['POST'])
def log_in():
    """Log In user."""

    email_entered = request.form.get('email')
    password_entered = request.form.get('password')
    
    user = crud.get_user_by_email(email_entered)

    if user is None:
        flash('This email address is not associated with an account. Please try again.')
    elif password_entered == user.password:
        # Send username to the session to be used elsewhere
        session['username'] = user.name 
        # Send user_id to the session to be used for database creation
        session['user_id'] = user.user_id 
        username = session['username']
        flash(f'You are successfully logged in, {username}!')
    else:
        flash('Incorrect password. Please try again.')

    return redirect('/')

@app.route('/users_choice')
def users_choice():
    """ Renders users_choice.html 
    
        This is the form that allows the user to choose num_branches, 
        num_points and num_rounds. Only display if there is a user logged in.
    """
    if session['username'] == None:
        flash("Please log in")
        return redirect('/')
    else: 
        return render_template('users_choice.html')

@app.route('/logout')
def log_out():
    """Log Out user."""

    user = session['username']

    if user is None:
        flash('Log in first.')
    else:
        # Reset username & user_id
        session['username'] = None
        session['user_id'] = None
        
        flash(f'You have been successfully logged out.')
  
    return redirect('/')

@app.route('/get_choices')
def get_choices():
    """ Get option choices from users_choice.html for snowflake pattern. 
    
        After the user chooses how many of each, this route will grab them,
        make them integers, and create the pattern database.
    """
 
    num_rounds = int(request.args.get('num_rounds'))
    num_branches = int(request.args.get('num_branches'))
    num_points = int(request.args.get('num_points'))

    pattern = crud.create_pattern(num_rounds, num_branches, num_points)

    # This for loop will call the crud functions that generate the random
    # rounds. Round 1 is always "ch6 to form a loop". The final round is the only 
    # one that needs to look at the number of branches. Rounds 2 through
    # (final round - 1) all need to have number of branches equal to zero.
    for rnd in range(2,(num_rounds +1)):
           
        if rnd != num_rounds:
            sfround_id = crud.choose_sfround(0, rnd)
        else:
            sfround_id = crud.choose_sfround(num_branches, rnd)
        pattern_round = crud.create_pattern_round(pattern.pattern_id, sfround_id)

        pattern_id = pattern.pattern_id
         
    return redirect(f'/patterns/{pattern_id}')

@app.route('/patterns')
def all_patterns():
    """ View all patterns """

    patterns = crud.get_patterns()

    return render_template('all_patterns.html', patterns=patterns)

@app.route('/patterns/<pattern_id>')
def show_pattern(pattern_id):
    """ Show details for a particular pattern """

    pattern = crud.get_pattern_by_id(pattern_id)
    sfrounds = crud.get_sfrounds_by_sfround_ids(pattern_id)
    return render_template('pattern_details.html', pattern=pattern, sfrounds=sfrounds)

@app.route('/user_patterns')
def all_patterns_for_user():
    """ View all patterns for a specific user """

    user_id = session['user_id']
    user_patterns = crud.get_patterns_by_user_id(user_id)
    
    return render_template('user_patterns.html', user_patterns=user_patterns)

@app.route("/completion_date.json")
def get_completion_date():
    """Get completion date."""

    pattern_id = request.args.get("pattern_id")
    completion_date = request.args.get("completion")
    pattern = crud.add_completion_date_to_pattern(pattern_id, completion_date)
    
    return jsonify({"completion":completion_date})

@app.route("/deletion")
def delete_pattern():
    """ Delete a pattern """

    pattern_id = request.args.get("pattern_id")
    pattern = crud.delete_pattern_with_pattern_id(pattern_id)

    return jsonify({"pattern_id":"Deleted"})  

@app.route("/add_photo")
def add_photo():
    """ Add a photo to the pattern """
    
    pattern_id = request.args.get("pattern_id")
    image_url = request.args.get("image_url")
    print('***ADD PHOTO***')
    print(image_url)
    image_public_id = request.args.get("image_public_id")
    image_format = request.args.get("image_format")
    
    resized_image_url = "https://res.cloudinary.com/dbjwx7sg5/image/upload/w_400,h_400/"+image_public_id+"."+image_format
    pattern = crud.add_photo_to_pattern(pattern_id, resized_image_url)

    return jsonify({"image_url":resized_image_url})

@app.route("/sort_by_completion")
def sort_by_completion():
    """ Sort patterns by completion date

        This allows the users to have their patterns sorted by their completion dates.
    """
    user_id = session['user_id']
    patterns = crud.get_patterns_by_user_id_sort_by_completion_date(user_id)
    print("***** SERVER.PY  sort by completion")
    print(f'patterns: {patterns}')
    return render_template('user_patterns_sorted.html', patterns=patterns)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='127.0.0.1', port=8000, debug=True)
