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
import json, random, string

# Import code to handle code sent from callback method
# flow_from_clientsecrets: creates a flow object from the client_secrets.json
# file
# FlowExchangeError: handles error trying to exchange authorization code for
# an access token
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

# Read in google auth info
CLIENT_ID = json.loads(open(
    'client_secrets.json', 'r').read())['web']['client_id']

# Read in facebook auth info
APP_ID = json.loads(open(
    'fb_client_secrets.json', 'r').read())['web']['app_id']

# Import Database code
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie, User

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

    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', client_id=CLIENT_ID, app_id=APP_ID,
        STATE=state)


# Create server-side function to handle google sign in callback
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # now that we confirm that the token the client sends to the server matches
    # the token that the server sent to the client
    # this helps make sure that the user is making the request and not a
    # malicious script
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Obtain authorization code
    code = request.data

    try:
        # upgrade the authorization code into a credentials object
        # create a oauth_flow object and add client_secret key info into it
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # Specify with 'postmessage' that this is the onetime code flow the
        # server will be sending off
        oauth_flow.redirect_uri = 'postmessage'
        # initiate the exchange and pass in the one time code
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
            % access_token)
    # Create a JSON GET request that contains the url and access token
    # Store the result of the request in a variable called result
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    # If this if statement is not True, then we know we have a working access
    # token
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Assuming none of the above if statements were True
    # Store the access token in the session for later use
    login_session['provider'] = 'google'  # ADD PROVIDER TO LOGIN SESSION
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    response = make_response(json.dumps('Successfully connected user'), 200)

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    # See if user exists, if it doesn't make a new one
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += (' " style="width: 300px; height:300px; border-radius: 150px;"'
                '" -webkit-border-radius: 150px; -moz-border-radius: 150px;">')

    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# Disconnect - revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # only disconnect connected users
    access_token = login_session.get('access_token')

    if access_token is None:
        print("Access token is None")
        response = make_response(json.dumps(
            'Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    print("In gdisconnect access token is %s" % access_token)
    print("Username is: %s" % login_session['username'])

    # Execute HTTP GET request to revoke current token
    url = ('https://accounts.google.com/o/oauth2/revoke2token=%s'
            % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    print("Result is: %s" % result)

    if result['status'] == '200':
        response = make_response(json.dumps(
            'Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'

        return response
    else:
        # For whatever reason, the given token was invalid
        response = make_response(json.dumps(
            'Failed to revoke token for given user', 400))
        response.headers['Content-Type'] = 'application/json'

        return response


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']

        flash("You have successfully been logged out.")

        return redirect(url_for('show_catalog'))
    else:
        flash("You were not logged in to begin with!")
        redirect(url_for('show_catalog'))


def getUserInfo(user_id):
    '''
        Gets User information.

        Params
            user_id (int): User id of user info to be retrieved

        Returns
            user (Object): User object with related information
    '''
    user = session.query(User).filter_by(id=user_id).one()

    return user


def getUserID(email):
    '''
        Gets User id.

        Params
            email (str): Email to check to obtain User id

        Returns
            user.id (int): Corresponding User's id
            None: If no email exists, None is returned
    '''
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def createUser(login_session):
    '''
        Creates new User in database extracting necessary fields necessary
        from login_session.

        Params
            login_session (dict): User data to be extracted

        Returns
            user.id (int): User id
    '''
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


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
    # Protect this page
    if 'username' not in login_session:
        return redirect('/login')

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

    # Protect this page
    if 'username' not in login_session:
        return redirect('/login')

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

    # Protect this page
    if 'username' not in login_session:
        return redirect('/login')

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
