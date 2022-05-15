from utils import validator

from database.models import Genre
from database.schemas import GenreSchema
from database.db import db
from flask_restx import Resource
from api import api
from flask import Blueprint, request

genres_module = Blueprint("genres", __name__)

genres_ns = api.namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenresViews(Resource):
    def get(self):

        try:
            with db.session.begin():
                genres_result = db.session.query(Genre)
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

        result = genres_schema.dump(genres_result)
        if len(result) == 0:
            return "Data not found", 404
        return result, 200

    def post(self):

        request_data = request.json

        # validating data
        validation_result = validator("POST", request_data, Genre, genre_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]

        # writing new data
        try:
            with db.session.begin():
                new_genre = Genre(**request_data)
                db.session.add(new_genre)
            return f"New data entry created successfully. Data ID: {new_genre.id}", 201
        except Exception as err:
            return f"Internal server error. Error: {err}", 500


@genres_ns.route('/<int:genre_id>')
class GenreViews(Resource):
    def get(self, genre_id: int):
        try:
            with db.session.begin():
                genre = db.session.query(Genre).get(genre_id)
                if genre is None:
                    return f"Data ID: {genre_id} not found.", 404
                result = genre_schema.dump(genre)
                return result
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

    def put(self, genre_id: int):
        try:
            with db.session.begin():
                genre = db.session.query(Genre).get(genre_id)
                if genre is None:
                    return f"Data ID: {genre_id} not found.", 404
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

        request_data = request.json

        # validating data
        validation_result = validator("PUT", request_data, Genre, genre_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]

        # writing new data
        try:
            with db.session.begin():
                genre = db.session.query(Genre).get(genre_id)

                for k, v in request_data.items():
                    setattr(genre, k, v)
                db.session.add(genre)
                return f"Data ID: {genre_id} was updated.", 200
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

    def patch(self, genre_id: int):
        try:
            with db.session.begin():
                genre = db.session.query(Genre).get(genre_id)
                if genre is None:
                    return f"Data ID: {genre_id} not found.", 404
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

        request_data = request.json

        validation_result = validator("PATCH", request_data, Genre, genre_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]

        # writing new data
        try:
            with db.session.begin():
                genre = db.session.query(Genre).get(genre_id)

                for k, v in request_data.items():
                    setattr(genre, k, v)
                db.session.add(genre)
                return f"Data ID: {genre_id} was partially updated.", 200
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

    def delete(self, genre_id: int):
        try:
            with db.session.begin():
                genre = db.session.query(Genre).get(genre_id)
                db.session.delete(genre)
                return f"Data ID: {genre_id} was deleted successfully.", 200
        except Exception as err:
            return f"Data ID: {genre_id} not found. Error: {err}", 404
