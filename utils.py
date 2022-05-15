from typing import Tuple, Dict, List, Any

from database.db import db
from marshmallow import ValidationError


def validator(method: str, request_data: Any, Obj: object, Obj_schema: object) \
        -> tuple[bool, str, int] | tuple[bool, dict[str, int | str | Any], int] | tuple[bool, None, None]:

    # validating data structure
    try:
        try:
            with db.session.begin():
                movie = db.session.query(Obj).first()
                movie_keys = set(Obj_schema.dump(db.session.query(Obj).first()).keys())
        except Exception as err:
            return True, f"Internal server error. Error: {err}", 500
        movie_keys.remove('id')
        data_keys = set(request_data.keys())
        if data_keys != movie_keys:
            messages = {}
            diff1 = movie_keys.difference(data_keys)
            diff2 = data_keys.difference(movie_keys)
            if method in ["PUT", "POST"]:
                for diff_entry in diff1:
                    messages[diff_entry] = "Missing field"
            for diff_entry in diff2:
                messages[diff_entry] = "Unknown field"
            if len(messages) > 0:
                raise ValidationError(message=messages)
    except ValidationError as err:
        error_text_entry = {"PUT": [" full", "Required"],
                            "POST": [" full", "Required"],
                            "PATCH": ["", "Available"]}
        return True, {"response_status_code": 422,
                      "response_status": "UNPROCESSABLE ENTITY",
                      "error_text": "Validation Error. Invalid structure found in request body data. {} request "
                                    "must contain only{} dataset with valid keys for successful processing. "
                                    "{} data keys: {}".format(method,
                                                              error_text_entry[method][0],
                                                              error_text_entry[method][1],
                                                              movie_keys),
                      "incorrect_data": err.messages}, 422

    if method == 'POST':
        # validating if database already contains data
        with db.session.begin():
            if Obj.__name__ == "Movie":
                query = db.session.query(Obj).filter(Obj.title == request_data['title'],
                                                       Obj.year == request_data['year'],
                                                       Obj.director_id == request_data['director_id']).first()
            else:
                query = db.session.query(Obj).filter(Obj.name == request_data['name']).first()
        query_data = Obj_schema.dump(query)
        if len(query_data) > 0:
            return True, f"Data already in database. Data ID: {query.id}", 400

    return False, None, None
