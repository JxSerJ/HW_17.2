from importlib import reload

from flask import Flask, request
from flask_restx.representations import output_json

from database.database import db
from api import api
from movies.views import movies_module
import sys

application = Flask(__name__)
application.config.from_pyfile("config.py")

api.app = application
api.init_app(application)
api.app.config['RESTFUL_JSON'] = {'ensure_ascii': False}
api.representations = {'application/json; charset=utf-8': output_json}

db.app = application
db.init_app(application)

application.register_blueprint(movies_module)

if __name__ == '__main__':
    application.run(debug=True)
