#!/usr/bin/env python3

# Here we set up the server to run our application

# Use these commands to check and free ports:
# sudo lsof -i :PORT
# kill -9 PID

from flask import Flask
app = Flask(__name__)


@app.route('/')
def show_catalog():
    return "I'm home!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
