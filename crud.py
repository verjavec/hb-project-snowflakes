import datetime
import random

from flask import Flask, flash, session
""" CRUD operations """
from model import db, User, connect_to_db, Pattern, Sfround, Pattern_round


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

def create_sfround(beg_seq, end_seq, sfround_no, sequence, seq_num_branches):
    """Create and return a new snowflake round."""

    sfround = Sfround(beg_seq=beg_seq, end_seq=end_seq, sequence=sequence, sfround_no=sfround_no, seq_num_branches=seq_num_branches)

    db.session.add(sfround)
    db.session.commit()

    return sfround

def create_pattern_round(pattern_id, sfround_id):
    """Create and return a new entry in the associative table."""

    pattern_round = Pattern_round(pattern_id=pattern_id, sfround_id=sfround_id)

    db.session.add(pattern_round)
    db.session.commit()

    return pattern_round

def create_pattern(num_rounds, num_branches, num_points):
    """Create and return a new pattern."""

    user_id = session['user_id']
    # user_id = 1  # FOR INITIAL TESTING
    
    pattern = Pattern(user_id=user_id, num_rounds=num_rounds, num_branches=num_branches, num_points=num_points)
    # print('**********')
    # print(f'num_rounds {num_rounds}, num_branches {num_branches}, num_points {num_points}')
    # print(pattern)
   
    db.session.add(pattern)
    db.session.commit()

    return pattern
    
# def get_all_repeaters_with_num_branches(num_branches):
#     """Return all repeaters with the required number of branches."""
    
#     return Repeater.query.filter(Repeater.repeater_num_branches == num_branches).all()

# def get_all_repeaters_for_round_no(num_rounds):
#     """ Return all repeaters with up to the required number of rounds."""

#     return Repeater.query.filter(Repeater.round_no == num_rounds).all()

def choose_sfround(num_branches, sfround_no):
    """ Return a random round that has the same number of branches the user chose.

        Since each round needs unique stitches, 
        this needs to be done for each round in the pattern.
        
        get_all_sfrounds_with_round_no_and_num_rounds is called to return
        a list of sequences for the current round with the number of branches 
        necessary.

        One is chosen randomly from that list to be the repeated stitch sequence
        for that round.

     """
    print('***!!choose_sfround!!***')
    print(num_branches, sfround_no)
    avail_sfrounds = get_all_sfrounds_with_sfround_no_and_num_branches(num_branches, sfround_no)
    sfround = random.choice(avail_sfrounds)
    sfround_id = sfround.sfround_id
    print(avail_sfrounds)

    return sfround_id

def get_all_sfrounds_with_sfround_no_and_num_branches(num_branches, sfround_no):
    """ Return all sfrounds that have both the round number 
            and the required number of branches. """
    
    avail_sfrounds = Sfround.query.filter((Sfround.sfround_no == sfround_no) 
                        & (Sfround.seq_num_branches == num_branches)).all()
    
    return avail_sfrounds    

def get_patterns():
    """ Return all of the patterns """

    return Pattern.query.all()

def get_pattern_by_id(pattern_id):
    """ Return all of the patterns with pattern_id """

    return Pattern.query.get(pattern_id)

def get_pattern_round_by_pattern_id(pattern_id):
    """ Return all pattern_rounds used for a specific pattern id """

    return Pattern_round.query.filter(Pattern_round.pattern_id == pattern_id).all()

def get_sfrounds_by_pattern_id(pattern_id):
    """ Return all sfrounds used for a specific pattern id """
    sfround_id_list = []
    pattern_rounds = get_pattern_round_by_pattern_id(pattern_id)
    
    for pattern_round in pattern_rounds:
        sfround_id = pattern_round.sfround_id
        # print('*****************')
        # print(sfround_id)
        sfround_id_list.append(sfround_id)
        # print('!!!!!!!!!!!!!!!')
        # print(sfround_id_list)
    
    return sfround_id_list    

def get_sfrounds_by_sfround_ids(pattern_id):
    sfrounds = []
    sfround_ids = get_sfrounds_by_pattern_id(pattern_id)
    
    for sfround_id in sfround_ids:
        sfround = Sfround.query.get(sfround_id)
        print('**********')
        print(sfround)
        sfrounds.append(sfround)
        
    return sfrounds
