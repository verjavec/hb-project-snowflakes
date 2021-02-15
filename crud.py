import datetime
from flask import Flask, flash, session
""" CRUD operations """
from model import db, User, connect_to_db, Pattern, SFRound, Repeater

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

def create_user(email, name, password):
    """Create and return a new user."""

    user = User(email=email, name=name, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """ Return all of the users """

    return User.query.all()

def get_user_by_id(user_id):
    """ Get a user using user_id and return the user """

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""
    
    return User.query.filter(User.email == email).first()

def create_sfround(beg_seq, end_seq, repeater_id):
    """Create and return a new snowflake round."""

    sfround = SFRound(beg_seq=beg_seq, end_seq=end_seq, repeater_id=repeater_id)

    db.session.add(sfround)
    db.session.commit()

    return sfround

def create_repeater(round_no, repeater_num_branches, sequence):
    """Create and return a new repeater."""

    repeater = Repeater(round_no=round_no, repeater_num_branches=repeater_num_branches, sequence=sequence)

    db.session.add(repeater)
    db.session.commit()

    return repeater



def create_pattern(num_rounds, num_branches, num_points):
    """Create and return a new pattern."""

    user_id = session['user_id']
    # user_id = 1  --- FOR INITIAL TESTING
    num_rounds = num_rounds
    num_branches = num_branches
    num_points = num_points
    round_id = 1
    
    pattern = Pattern(user_id=user_id, num_rounds=num_rounds, num_branches=num_branches, num_points=num_points, round_id=round_id)
    # print('**********')
    # print(f'num_rounds {num_rounds}, num_branches {num_branches}, num_points {num_points}')
    # print(pattern)
   
    db.session.add(pattern)
    db.session.commit()

    return pattern
