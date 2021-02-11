""" This seeds the database for testing """

import os
import json

from random import choice, randint
from datetime import datetime

import crud
import model
import server

# Always want to start with a clean database for testing
os.system('dropdb snowflakes')
os.system('createdb snowflakes')

# Connect to database and create it
model.connect_to_db(server.app)
model.db.create_all()

with open('data/sequences.json') as f:
    sequence_data = json.loads(f.read())

rounds_in_db = []
repeaters_in_db = []
r = 1

for sfround in sequence_data:
   
    round_no = sfround['round_no']
    num_branches = sfround['num_branches']
    beg_seq = sfround['beg_seq']
    sequence = sfround['sequence']
    end_seq = sfround['end_seq']
    repeater_id = r
    print('**********')
    print(r)
    
    db_repeaters=crud.create_repeater(round_no, num_branches, sequence)
    repeaters_in_db.append(db_repeaters)
    
    db_sfround=crud.create_sfround(beg_seq, end_seq, repeater_id)
    rounds_in_db.append(db_sfround)
    r += 1

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    name = f'User{n}'
    password = 'test'

    user=crud.create_user(email, name, password)


    
    

