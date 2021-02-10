""" Server for Snowflake patterns. """

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """ View homepage """

    return render_template('homepage.html')

### --- This will be needed when I'm ready to start testing pattern listing 
# @app.route('/patterns')
# def all_movies():
#     """ View all movies """

#     patterns = crud.get_patterns()

#     return render_template('all_patterns.html', movies=patterns)

### --- This will be needed when I'm ready to start testing pattern details
# @app.route('/patterns/<pattern_id>')
# def show_pattern(pattern_id):
#     """ Show details for a particular pattern """

#     pattern = crud.get_pattern_by_id(pattern_id)
#     return render_template('pattern_details.html', pattern=pattern)

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
        flash('Cannot create an account with that email. Try again.')
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
        session['primary_key'] = user.user_id 
        flash('You are successfully logged in!')
    else:
        flash('Incorrect password. Please try again.')

    return redirect('/')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
