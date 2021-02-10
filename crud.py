import datetime

""" CRUD operations """
from model import db, User, connect_to_db, Pattern

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
