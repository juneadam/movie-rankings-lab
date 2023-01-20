"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# run these commands in the terminal
os.system('dropdb ratings')
os.system('createdb ratings')

# run these functions from model.py
model.connect_to_db(server.app)
model.db.create_all()

# open json file, save to variable f, load file data into dictionary movie_data
# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime
    title, overview, poster_path = (
        movie["title"],
        movie["overview"],
        movie["poster_path"],
    )

    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    # create a Movie object db_movie and append it to the movies_in_db list
    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(db_movie)

# add and commit the movies_in_db list of objects to the DB
model.db.session.add_all(movies_in_db)
model.db.session.commit()
# loop that generates ten user objects
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    # create a User object with above data
    new_user = crud.create_user(email, password)

    # create 10 ratings for the user
    for x in range(10):
        score = randint(1,5)
        movie = choice(movies_in_db)
        # calls creat_rating function to create new rating with random score
        # and movie and saves to variable rand_rating
        rand_rating = crud.create_rating(new_user, movie, score)
        # appends new_user.ratings list with rand_rating object
        new_user.ratings.append(rand_rating)

    model.db.session.add(new_user)


model.db.session.commit()    


