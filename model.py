""" Models for snowflake patterns """

from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    # patterns = a list of pattern objects

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.name} email={self.email}>'


class Pattern(db.Model):
    """A pattern."""

    __tablename__ = 'patterns'

    pattern_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    completion_date = db.Column(db.DateTime)
    num_rounds = db.Column(db.Integer)
    num_branches = db.Column(db.Integer)
    num_points = db.Column(db.Integer)
    round_id = db.Column(db.Integer, db.ForeignKey('rounds.round_id'))

    sfround = db.relationship('SFRound', backref='patterns')
    user = db.relationship('User', backref='patterns')

    def __repr__(self):
        return f'<Pattern pattern_id={self.pattern_id} num_rounds={self.num_rounds}>'

class SFRound(db.Model):
    """A round."""

    __tablename__ = 'rounds'

    round_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    beg_seq = db.Column(db.String)
    end_seq = db.Column(db.String)
    repeater_id = db.Column(db.Integer, db.ForeignKey('repeaters.repeater_id'))

    repeater = db.relationship('Repeater', backref='rounds')

    # patterns = a list of pattern objects

    def __repr__(self):
        return f'<Round round_id={self.round_id} beg_seq={self.beg_seq}>'

class Repeater(db.Model):
    """A repeater."""

    __tablename__ = 'repeaters'

    repeater_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    sequence = db.Column(db.Text)
    round_no = db.Column(db.Integer)
    repeater_num_branches = db.Column(db.Integer)

    # rounds = a list of sfround objects

    def __repr__(self):
        return f'<Repeater repeater_id={self.repeater_id} round_no={self.round_no}>'


def connect_to_db(flask_app, db_uri='postgresql:///snowflakes', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app