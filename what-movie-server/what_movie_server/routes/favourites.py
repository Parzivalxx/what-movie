from flask import make_response
from flask_pydantic import validate

from what_movie_server.schemas import (
    CreatePayloadPostRequest,
    CreateSuccessPostResponse,
    ReadSuccessGetResponse,
    FavouritesErrorResponse,
    UpdatePayloadPutRequest,
    UpdateSuccessPutResponse,
    DeleteSuccessDeleteResponse,
    ListSuccessGetResponse,
)
from what_movie_server.models import User, Favourites
from what_movie_server.routes import favourites_blueprint
from what_movie_server.app import db


@favourites_blueprint.route("/favourites", methods=["POST"])
@validate()
def create_favourite(body: CreatePayloadPostRequest):
    """
    Add favourite resource
    """
    try:
        # check if user does not exist
        user = User.query.filter_by(id=body.user_id).first()
        if not user:
            response_object = {"status": "fail", "message": "User does not exist."}
            return (
                make_response(
                    FavouritesErrorResponse.parse_obj(response_object).dict()
                ),
                404,
            )

        # check if favourite already exists
        existing_favourite = Favourites.query.filter_by(**body).first()
        if existing_favourite:
            response_object = {
                "status": "fail",
                "message": f"This favourite already exists: {existing_favourite.id}",
            }
            return (
                make_response(
                    FavouritesErrorResponse.parse_obj(response_object).dict()
                ),
                409,
            )

        # create new Favourites object
        favourite = Favourites(**body)

        # insert the favourite
        db.session.add(favourite)
        db.session.commit()
        response_object = {
            "status": "success",
            "message": f"Favourite {favourite.id} added successfully",
        }
        return (
            make_response(CreateSuccessPostResponse.parse_obj(response_object).dict()),
            201,
        )
    except Exception as e:
        response_object = {
            "status": "fail",
            "message": "Some error occurred. Please try again.",
        }
        return (
            make_response(FavouritesErrorResponse.parse_obj(response_object).dict()),
            401,
        )


@favourites_blueprint.route("/favourites/<favourite_id>", methods=["GET"])
@validate()
def read_favourite(favourite_id: int):
    """
    Read favourite resource
    """
    favourite = Favourites.query.filter_by(id=favourite_id).first()

    if not favourite:
        # Handle the case when the favourite is not found
        response_object = {
            "status": "fail",
            "message": f"Favourite does not exist: {favourite_id}",
        }
        return (
            make_response(FavouritesErrorResponse.parse_obj(response_object).dict()),
            404,
        )

    favourite_model = Favourites(**favourite)

    # Return the updated favourite as the response
    response_object = {
        "status": "success",
        "message": f"Favourite {favourite_id} updated successfully",
        "data": favourite_model.to_dict(),
    }

    return make_response(ReadSuccessGetResponse.parse_obj(response_object).dict()), 200


@favourites_blueprint.route("/favourites/<favourite_id>", methods=["PUT"])
@validate()
def update_favourite(favourite_id: int, body: UpdatePayloadPutRequest):
    favourite = Favourites.query.filter_by(id=favourite_id).first()

    if not favourite:
        # Handle the case when the favourite is not found
        response_object = {
            "status": "fail",
            "message": f"Favourite does not exist: {favourite_id}",
        }
        return (
            make_response(FavouritesErrorResponse.parse_obj(response_object).dict()),
            404,
        )

    favourite.update(**body.dict(exclude_unset=True))
    db.session.commit()

    # Return the updated favourite as the response
    response_object = {
        "status": "success",
        "message": f"Favourite {favourite_id} updated successfully",
        "data": favourite.to_dict(),
    }

    return (
        make_response(UpdateSuccessPutResponse.parse_obj(response_object).dict()),
        200,
    )


@favourites_blueprint.route("/favourites/<favourite_id>", methods=["DELETE"])
@validate()
def delete_favourite(favourite_id: int):
    favourite = Favourites.query.filter_by(id=favourite_id).first()

    if not favourite:
        # Favourite not found, return error response
        response_object = {
            "status": "fail",
            "message": f"Favourite does not exist: {favourite_id}",
        }
        return (
            make_response(FavouritesErrorResponse.parse_obj(response_object).dict()),
            404,
        )

    # Delete the favourite from the database
    db.session.delete(favourite)
    db.session.commit()

    # Return success response
    response_object = {
        "status": "success",
        "message": f"Favourite {favourite_id} deleted successfully",
    }
    return make_response(
        DeleteSuccessDeleteResponse.parse_obj(response_object.dict()), 200
    )


@favourites_blueprint.route("/favourites/<user_id>", methods=["GET"])
@validate()
def list_favourites(user_id: int):
    favourites = Favourites.query.filter_by(user_id=user_id).all()

    # Convert the favourites to a list of dictionaries
    favourites_list = [favourite.to_dict() for favourite in favourites]

    # Return the list of favourites as the response
    response_object = {
        "status": "success",
        "message": "Favourites retrieved successfully",
        "data": favourites_list,
    }
    return make_response(ListSuccessGetResponse.parse_obj(response_object).dict()), 200
