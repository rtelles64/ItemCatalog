#!/usr/bin/env python3

# Here we set up the server to run our application

# Use these commands to check and free ports:
# sudo lsof -i :PORT
# kill -9 PID

# Set up Flask
from flask import Flask
app = Flask(__name__)

# Import Database code
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def show_catalog():
    # To test, take out the first genre from our database
    genres = session.query(Genre)

    output = ''
    # Test output to see we can retrieve info
    for genre in genres:
        output += genre.name
        output += '</br>'

    return output

# Remember to include trailing '/' since flask will handle if the user omits it
@app.route('/catalog/<genre>/movies/')
def show_movies(genre):
    # EDGE CASE: Science Fiction (will have to be input as science-fiction)
    if '-' in genre:
        genre = genre.replace('-', ' ')

    # Capitalize genre input since that's how they are stored
    genre = genre.title()
    # Query database for genre and just extract genre object
    genre = session.query(Genre).filter_by(name=genre).one()

    # List out all of the movies in that genre
    movies = session.query(Movie).filter_by(genre=genre)

    output = ''

    # Print output
    for movie in movies:
        output += movie.name
        output += '</br>'

    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
