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

@app.route('/patterns')
def all_patterns():
    """ View all patterns """

    patterns = crud.get_patterns()

    return render_template('all_patterns.html', patterns=patterns)

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
        flash('Account with that email already exists. Try again.')
    else:
        crud.create_user(email, name, password)
        flash('Account created! Please log in.')

    return redirect('/')

@app.route('/', methods=['POST'])
def log_in():
    """Log In user."""

    # session['current_user'] = username
    #         flash(f'Logged in as {username}')
    #         return redirect('/')

    #     else:
    #         flash('Wrong password!')
    #         return redirect('/login')


    email_entered = request.form.get('email')
    password_entered = request.form.get('password')
    
    user = crud.get_user_by_email(email_entered)

    if user is None:
        flash('This email address is not associated with an account. Please try again.')
    elif password_entered == user.password:
        session['username'] = user.name 
        session['user_id'] = user.user_id
        username = session['username']
        # user_id = session['user_id']
        flash(f'You are successfully logged in, {username}!')
    else:
        flash('Incorrect password. Please try again.')

    return redirect('/')

@app.route('/users_choice')
def users_choice():
    """ Renders users_choice.html """
    
    return render_template('users_choice.html')

@app.route('/get_choices')
def get_choices():
    """ Get option choices from users_choice.html for snowflake pattern. """
    
    
    num_rounds = request.args.get('num_rounds')
    num_branches = request.args.get('num_branches')
    num_points = request.args.get('num_points')
    
    pattern = crud.create_pattern(num_rounds, num_branches, num_points)
            
    return redirect('/users_choice')

# @app.route('/api/choices/<int:pattern_id>')
# def get_pattern_by_id(pattern_id):
#     """Return a pattern from the database as JSON."""

#     pattern = Pattern.query.get(pattern_id)

#     if pattern:
#         return jsonify({'status': 'success',
#                         'pattern_id': pattern.pattern_id,
#                         'user_id': pattern.user_id,
#                         'date_completed': pattern.date_completed,
#                         'num_rounds': pattern.num_rounds,
#                         'num_points': pattern.num_points,
#                         'num_branches': pattern.num_branches
#                         'round_id': pattern.round_id})
#     else:
#         return jsonify({'status': 'error',
#                         'message': 'No pattern found with that ID'})



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='127.0.0.1', port=8000, debug=True)
