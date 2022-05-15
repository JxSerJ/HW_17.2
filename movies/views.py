from utils import validator

from database.models import Movie
from database.schemas import MovieSchema
from database.db import db
from flask_restx import Resource
from api import api
from flask import Blueprint, request

movies_module = Blueprint("movies", __name__)

movies_ns = api.namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesViews(Resource):
    def get(self):

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies_result = db.session.query(Movie)
        db.session.close()

        if director_id:
            movies_result = movies_result.filter(Movie.director_id == director_id)
        if genre_id:
            movies_result = movies_result.filter(Movie.genre_id == genre_id)
        movies_result = movies_result.all()

        result = movies_schema.dump(movies_result)
        if len(result) == 0:
            return "Data not found", 404
        return result, 200

    def post(self):

        request_data = request.json

        # validating data
        validation_result = validator("POST", request_data, Movie, movie_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]

        # writing new data
        try:
            with db.session.begin():
                new_movie = Movie(**request_data)
                db.session.add(new_movie)
            return f"New data entry created successfully. Data ID: {new_movie.id}", 201
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

        # movie_keys_all = set(vars(Movie).keys())  # returns all keys, including references from other tables. Archived
        # movie_keys = [key for key in movie_keys_all if not '__' in key and not '_sa' in key]  # Archived


@movies_ns.route('/<int:movie_id>')
class MovieViews(Resource):
    def get(self, movie_id: int):
        try:
            with db.session.begin():
                movie = db.session.query(Movie).get(movie_id)
                if movie is None:
                    return f"Data ID: {movie_id} not found.", 404
                result = movie_schema.dump(movie)
                return result
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

    def put(self, movie_id: int):
        try:
            with db.session.begin():
                movie = db.session.query(Movie).get(movie_id)
                if movie is None:
                    return f"Data ID: {movie_id} not found.", 404
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

        request_data = request.json

        # validating data
        validation_result = validator("PUT", request_data, Movie, movie_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]

        # writing new data
        try:
            with db.session.begin():
                movie = db.session.query(Movie).get(movie_id)

                for k, v in request_data.items():
                    setattr(movie, k, v)
                db.session.add(movie)
                return f"Data ID: {movie_id} was updated.", 200
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

    def patch(self, movie_id: int):
        try:
            with db.session.begin():
                movie = db.session.query(Movie).get(movie_id)
                if movie is None:
                    return f"Data ID: {movie_id} not found.", 404
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

        request_data = request.json

        validation_result = validator("PATCH", request_data, Movie, movie_schema)
        if validation_result[0]:
            return validation_result[1], validation_result[2]

        # writing new data
        try:
            with db.session.begin():
                movie = db.session.query(Movie).get(movie_id)

                for k, v in request_data.items():
                    setattr(movie, k, v)
                db.session.add(movie)
                return f"Data ID: {movie_id} was partially updated.", 200
        except Exception as err:
            return f"Internal server error. Error: {err}", 500

    def delete(self, movie_id: int):
        try:
            with db.session.begin():
                movie = db.session.query(Movie).get(movie_id)
                db.session.delete(movie)
                return f"Data ID: {movie_id} was deleted successfully.", 200
        except Exception as err:
            return f"Data ID: {movie_id} not found. Error: {err}", 404
