from flask import request, make_response, jsonify

from what_movie_server.models import User, Favourites
from what_movie_server.routes import favourites_blueprint
from what_movie_server.app import db


@favourites_blueprint.route("/favourites", methods=["POST"])
def create_favourite():
    """
    Add favourite resource
    """
    # get the post data
    post_data = request.get_json()
    try:
        # check if user does not exist
        user = User.query.filter_by(id=post_data.get("user_id")).first()
        if not user:
            response_object = {"status": "fail", "message": "User does not exist."}
            return make_response(jsonify(response_object)), 404

        # check if favourite already exists
        existing_favourite = Favourites.query.filter_by(**post_data).first()
        if existing_favourite:
            response = {
                "message": "This favourite already exists",
                "favourite_id": existing_favourite.id,
            }
            return make_response(jsonify(response)), 409

        # create new Favourites object
        favourite = Favourites(**post_data)

        # insert the favourite
        db.session.add(favourite)
        db.session.commit()
        response_object = {
            "message": "Favorite added successfully",
            "favourite_id": favourite.id,
        }
        return make_response(jsonify(response_object)), 201
    except Exception as e:
        response_object = {
            "status": "fail",
            "message": "Some error occurred. Please try again.",
        }
        return make_response(jsonify(response_object)), 401
