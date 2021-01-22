import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, Movie, Actor

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/')
def index():
    return "Hello World"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
