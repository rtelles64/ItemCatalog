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
    genre = session.query(Genre).first()
    # List out all of the movies in that genre
    movies = session.query(Movie).filter_by(genre_id=genre.id)

    output = ''
    # Test output to see we can retrieve info
    for movie in movies:
        output += movie.name
        output += '</br>'
        output += movie.description
        output += '</br></br>'

    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
