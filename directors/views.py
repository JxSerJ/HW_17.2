from utils import validator

from database.models import Director
from database.schemas import DirectorSchema
from database.db import db
from flask_restx import Resource
from api import api
from flask import Blueprint, request

directors_module = Blueprint("directors", __name__)

directors_ns = api.namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorsViews(Resource):
    def get(self):

        try:
            with db.session.begin():
                directors_result = db.session.query(Director)
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

        result = directors_schema.dump(directors_result)
        if len(result) == 0:
            return "Data not found", 404
        return result, 200

    def post(self):

        request_data = request.json

        # validating data
        validation_result = validator("POST", request_data, Director, director_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]

        # writing new data
        try:
            with db.session.begin():
                new_director = Director(**request_data)
                db.session.add(new_director)
            return f"New data entry created successfully. Data ID: {new_director.id}", 201
        except Exception as err:
            return f"Internal server error. Error: {err}", 500


@directors_ns.route('/<int:director_id>')
class DirectorViews(Resource):
    def get(self, director_id: int):
        try:
            with db.session.begin():
                director = db.session.query(Director).get(director_id)
                if director is None:
                    return f"Data ID: {director_id} not found.", 404
                result = director_schema.dump(director)
                return result
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

    def put(self, director_id: int):
        try:
            with db.session.begin():
                director = db.session.query(Director).get(director_id)
                if director is None:
                    return f"Data ID: {director_id} not found.", 404
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

        request_data = request.json

        # validating data
        validation_result = validator("PUT", request_data, Director, director_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]

        # writing new data
        try:
            with db.session.begin():
                director = db.session.query(Director).get(director_id)

                for k, v in request_data.items():
                    setattr(director, k, v)
                db.session.add(director)
                return f"Data ID: {director_id} was updated.", 200
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

    def patch(self, director_id: int):
        try:
            with db.session.begin():
                director = db.session.query(Director).get(director_id)
                if director is None:
                    return f"Data ID: {director_id} not found.", 404
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

        request_data = request.json

        validation_result = validator("PATCH", request_data, Director, director_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]

        # writing new data
        try:
            with db.session.begin():
                director = db.session.query(Director).get(director_id)

                for k, v in request_data.items():
                    setattr(director, k, v)
                db.session.add(director)
                return f"Data ID: {director_id} was partially updated.", 200
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

    def delete(self, director_id: int):
        try:
            with db.session.begin():
                director = db.session.query(Director).get(director_id)
                db.session.delete(director)
                return f"Data ID: {director_id} was deleted successfully.", 200
        except Exception as err:
            return f"Data ID: {director_id} not found. Error: {err}", 404
