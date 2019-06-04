#!/usr/bin/env python3

# Here we set up the server to run our application

# Use these commands to check and free ports:
# sudo lsof -i :PORT
# kill -9 PID

# Set up Flask
from flask import (flash, Flask, jsonify, redirect, render_template, request,
                    url_for)
app = Flask(__name__)

# Add imports for authentication and authorization
from flask import session as login_session
import random, string

# Import Database code
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create state token to prevent request forgery
# Store it in session for later validation
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state

    return "The current session state is %s" % login_session['state']
# Say there's a web app that wants to collect our data
#
# The app wants to see genre and movie info but doesn't want need to parse
# through html or waste bandwidth receiving css files
#
# For this reason we have APIs, that allow external apps to use public info
# our apps want to share without bells and whistles
#
# When an API is communicated over the internet, following the rules of HTTP,
# this is a RESTful API
#
# The most popular ways of sending data with a RESTful architecure is with
# JSON format
#
# Here we include the JSON format implementation


# API ENDPOINTS
# Genres JSON
@app.route('/catalog.json')
def catalog_json():
    genres = session.query(Genre)

    return jsonify(Genres=[i.serialize for i in genres])


# Movies per Genre JSON
@app.route('/catalog/<int:genre_id>/movies.json')
def movies_json(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(genre_id=genre.id)

    return jsonify(Movies=[i.serialize for i in movies])


# Single movie JSON
@app.route('/catalog/<int:movie_id>.json')
def solo_json(movie_id):
    movie = session.query(Movie).filter_by(id=movie_id).one()

    return jsonify(Movie=movie.serialize)


# Show (READ) genres
@app.route('/catalog/')
@app.route('/')
def show_catalog():
    # To test, take out the first genre from our database
    genres = session.query(Genre)

    # output = ''
    # Test output to see we can retrieve info
    # for genre in genres:
    #     output += genre.name
    #     output += '</br>'

    return render_template('home.html', genres=genres)


# Show (READ) movies of selected genre
# Remember to include trailing '/' since flask will handle if the user omits it
@app.route('/catalog/<int:genre_id>/movies/')
def show_movies(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    # List out all of the movies in that genre
    movies = session.query(Movie).filter_by(genre_id=genre.id)
    # Get number of movies based on genre
    num_movies = session.query(Movie).filter_by(genre_id=genre.id).count()

    # output = ''
    #
    # output += genre.name + '</br></br>'
    #
    # # Print output
    # for movie in movies:
    #     output += movie.name
    #     output += '</br>'
    #
    # return output
    return render_template('genre.html', genre=genre, movies=movies,
                           length=num_movies, genre_id=genre_id)


# Show (READ) selected movie info
@app.route('/catalog/<int:genre_id>/<int:movie_id>/')
def get_movie(genre_id, movie_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movie = session.query(Movie).filter_by(id=movie_id).one()

    # output = ''
    #
    # for film in movie:
    #     output += film.name
    #     output += '</br>'
    #     output += film.description
    #     output += '</br></br>'
    #
    # return output
    return render_template('movie.html', genre=genre, movie=movie,
                            genre_id=genre_id)


# Add (CREATE) movie
@app.route('/catalog/<int:genre_id>/new/', methods=['GET', 'POST'])
def new_movie(genre_id):
    if request.method == 'POST':
        newMovie = Movie(name=request.form['name'], genre_id=genre_id)
        session.add(newMovie)
        session.commit()

        # Let user know movie was successfully created
        flash("New movie created!")

        return redirect(url_for('show_movies', genre_id=genre_id))
    else:
        return render_template('newMovie.html', genre_id=genre_id)


# Edit (UPDATE) Movie
@app.route('/catalog/<int:genre_id>/<int:movie_id>/edit/',
            methods=['GET', 'POST'])
def edit_movie(genre_id, movie_id):
    edit_movie = session.query(Movie).filter_by(id=movie_id).one()

    if request.method == 'POST':
        if request.form['name']:
            edit_movie.name = request.form['name']
        if request.form['description']:
            edit_movie.description = request.form['description']

        session.add(edit_movie)
        session.commit()

        # Let user know movie was successfully edited
        flash("Movie edited!")

        return redirect(url_for('get_movie', genre_id=genre_id,
                                movie_id=movie_id))
    else:
        return render_template('editMovie.html', genre_id=genre_id,
                                movie_id=movie_id, i=edit_movie)


# DELETE Movie
@app.route('/catalog/<int:genre_id>/<int:movie_id>/delete/',
            methods=['GET', 'POST'])
def delete_movie(genre_id, movie_id):
    delete_movie = session.query(Movie).filter_by(id=movie_id).one()

    if request.method == 'POST':
        session.delete(delete_movie)
        session.commit()

        # Let user know movie was deleted successfully
        flash("Movie deleted!")

        return redirect(url_for('show_movies', genre_id=genre_id))
    else:
        return render_template('deleteMovie.html', i=delete_movie)


if __name__ == '__main__':
    # Add flash functionality
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
