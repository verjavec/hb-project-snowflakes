""" This seeds the database """

import os
import json

from random import choice, randint
from datetime import date, datetime

import crud
import model
import server

# Always want to start with a clean database for testing
os.system('dropdb snowflakes')
os.system('createdb snowflakes')

# Connect to database and create it
model.connect_to_db(server.app)
model.db.create_all()

# Open the .json file with the snowflake pattern data
with open('data/sequences.json') as f:
    sequence_data = json.loads(f.read())

sfrounds_in_db = []

# collect the data from the .json file and assign it to variables
for sfround in sequence_data:
   
    sfround_no = sfround['sfround_no']
    seq_num_branches = sfround['seq_num_branches']
    beg_seq = sfround['beg_seq']
    sequence = sfround['sequence']
    end_seq = sfround['end_seq']
    
    db_sfround=crud.create_sfround(beg_seq, end_seq, sfround_no, sequence, seq_num_branches)
    sfrounds_in_db.append(db_sfround)

# Create user database for testing    
for n in range(5):
    email = f'user{n}@test.com'  
    name = f'User{n}'
    password = 'test'

    user=crud.create_user(email, name, password)


    
    

