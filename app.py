# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from marshmallow import Schema, fields
from database.database import db

app = Flask(__name__)
app.config.from_pyfile("config.py")

api = Api(app)

movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

# TODO create blue prints (JFF)





if __name__ == '__main__':
    app.run(debug=True)
