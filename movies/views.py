from database.models import Movie
from database.schemas import MovieSchema
from database.database import db
from flask_restx import Resource
from api import api
from flask import Blueprint, request, jsonify, current_app


movies_module = Blueprint("movies", __name__)

movies_ns = api.namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesViews(Resource):
    def get(self):
        with db.session.begin():
            all_movies = db.session.query(Movie).all()
        result = movies_schema.dump(all_movies)
        return result, 200

    def post(self):
        data = request.json
        with db.session.begin():
            new_movie = Movie(**data)
            db.session.add(new_movie)
        return "New data added", 201


@movies_ns.route('/<int:movie_id>')
class MovieViews(Resource):
    def get(self, movie_id: int):
        with db.session.begin():
            db_query = Movie.query.get(movie_id)
        result = movie_schema.dump(db_query)
        return result

    def put(self, movie_id: int):
        reqest_data = request.json
        # TODO validation if all keys included
        try:
            movie = db.session.query(Movie).get(movie_id)
        except Exception as err:
            return f"Data ID:{movie_id} not found. Error: {err}", 404
        movie = movie_schema.load(reqest_data)
        with db.session.begin():
            db.session.add(movie)
        return f"Data ID:{movie_id} was updated \nNew data: {movie_schema.dumps(movie)}", 200

    def patch(self, movie_id: int):
        pass

    def delete(self, movie_id: int):
        pass
