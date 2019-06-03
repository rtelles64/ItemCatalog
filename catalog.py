#!/usr/bin/env python3

# Here we set up the server to run our application

# Use these commands to check and free ports:
# sudo lsof -i :PORT
# kill -9 PID

# Set up Flask
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)

# Import Database code
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


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

        return redirect(url_for('show_movies', genre_id=genre_id))
    else:
        return render_template('deleteMovie.html', i=delete_movie)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
