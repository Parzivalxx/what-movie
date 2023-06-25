from flask import make_response
from flask_pydantic import validate

from what_movie_server.schemas import (
    ReadUserSuccessGetResponse,
    DeleteUserSuccessDeleteResponse,
    ListUsersSuccessGetResponse,
    UsersErrorResponse,
    UserSchema,
)
from what_movie_server.models import User
from what_movie_server.routes import users_blueprint
from what_movie_server.app import db


@users_blueprint.route("/users/<email>", methods=["GET"])
@validate()
def read_user(email: str):
    """
    Read user resource
    """
    user = User.query.filter_by(email=email).first()

    if not user:
        # Handle the case when the user is not found
        response_object = {
            "status": "fail",
            "message": f"User does not exist: {email}",
        }
        return (
            make_response(UsersErrorResponse.parse_obj(response_object).dict()),
            404,
        )

    # Return the updated favourite as the response
    response_object = {
        "status": "success",
        "data": UserSchema.from_orm(user),
    }

    return make_response(ReadUserSuccessGetResponse.parse_obj(response_object).dict()), 200


@users_blueprint.route("/users/<user_id>", methods=["DELETE"])
@validate()
def delete_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        # User not found, return error response
        response_object = {
            "status": "fail",
            "message": f"User does not exist: {user_id}",
        }
        return (
            make_response(UsersErrorResponse.parse_obj(response_object).dict()),
            404,
        )

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    # Return success response
    response_object = {
        "status": "success",
        "message": f"User {user_id} deleted successfully",
    }
    return (
        make_response(DeleteUserSuccessDeleteResponse.parse_obj(response_object).dict()),
        200,
    )


@users_blueprint.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()

    # Convert the users to a list of User schemas
    users = [UserSchema.from_orm(user) for user in users]

    # Return the list of favourites as the response
    response_object = {
        "status": "success",
        "data": users,
    }
    return make_response(ListUsersSuccessGetResponse.parse_obj(response_object).dict()), 200
