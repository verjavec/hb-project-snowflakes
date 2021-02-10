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



for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    name = f'User{n}'
    password = 'test'

    user=crud.create_user(email, name, password)


    
    

