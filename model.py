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
    
    user = db.relationship('User', backref='patterns')

    def __repr__(self):
        return f'<Pattern pattern_id={self.pattern_id} num_rounds={self.num_rounds}>'

class Sfround(db.Model):
    """A snowflake round."""

    __tablename__ = 'sfrounds'

    sfround_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    beg_seq = db.Column(db.Text)
    end_seq = db.Column(db.Text)
    sfround_no = db.Column(db.Integer)
    sequence = db.Column(db.Text)
    seq_num_branches = db.Column(db.Integer)

    def __repr__(self):
        return f'<Sfround sfround_id={self.sfround_id} beg_seq={self.beg_seq} end_seq={self.end_seq} seq_mum_branches={self.seq_num_branches}>'

class Pattern_round(db.Model):
    """An associative table to connect sfrounds and patterns."""

    __tablename__ = 'patterns_rounds'

    pattern_round_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    pattern_id = db.Column(db.Integer, db.ForeignKey('patterns.pattern_id'))
    sfround_id = db.Column(db.Integer, db.ForeignKey('sfrounds.sfround_id'))

    pattern = db.relationship('Pattern', backref='patterns_rounds')
    sfround = db.relationship('Sfround', backref='patterns_rounds')
    
    def __repr__(self):
        return f'<Pattern_round pattern_round_id={self.pattern_round_id}>'

def connect_to_db(flask_app, db_uri='postgresql:///snowflakes', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app