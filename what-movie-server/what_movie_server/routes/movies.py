from flask import make_response, jsonify, request
from http import HTTPStatus
import requests

from what_movie_server.routes import movies_blueprint
from what_movie_server.routes.decorators import add_request_headers
from what_movie_server.models import (
    NowshowingGetRequest,
    NowshowingGetResponse,
    ComingsoonGetRequest,
    ComingsoonGetResponse,
    ShowtimesGetRequest,
    ShowtimesGetResponse,
)
from what_movie_server.app import app


BASE_MOVIEGLU_URL = app.config["BASE_MOVIEGLU_URL"]
REQUEST_RETRIES = app.config["REQUEST_RETRIES"]


def get_request(headers, route_name, request_cls, response_cls):
    """Helper function to perform get request to MovieGlu API"""
    request_data = request_cls(**request.args.to_dict())
    for _ in range(REQUEST_RETRIES):
        try:
            response = requests.get(
                f"{BASE_MOVIEGLU_URL}{route_name}/",
                params=request_data.dict(),
                headers=headers,
            )
            status_code = response.status_code
            if status_code == HTTPStatus.OK:
                return (
                    make_response(response_cls.parse_obj(response.json()).dict()),
                    200,
                )
            elif status_code == HTTPStatus.NO_CONTENT:
                return make_response([]), 204
            else:
                app.logger.warning(f"Unaccepted status code received: {status_code}")
                continue
        except Exception as e:
            app.logger.error(e, exc_info=True)
            continue
    app.logger.error("Request run time error")
    response_object = {
        "message": f"Request timed out, attempted {REQUEST_RETRIES} times"
    }
    return make_response(jsonify(response_object)), 408


@movies_blueprint.route("/movies/nowshowing", methods=["GET"])
@add_request_headers
def get_movies_now_showing(headers=None):
    """
    Retrieve the currently showing movies
    """
    return get_request(
        route_name="filmsNowShowing",
        headers=headers,
        request_cls=NowshowingGetRequest,
        response_cls=NowshowingGetResponse,
    )


@movies_blueprint.route("/movies/comingsoon", methods=["GET"])
@add_request_headers
def get_movies_coming_soon(headers=None):
    """
    Retrieve the movies coming soon
    """
    return get_request(
        route_name="filmsComingSoon",
        headers=headers,
        request_cls=ComingsoonGetRequest,
        response_cls=ComingsoonGetResponse,
    )


@movies_blueprint.route("/movies/showtimes", methods=["GET"])
@add_request_headers
def get_movies_showtimes(headers=None):
    """
    Retrieve the showtimes for a selected movie and date
    """
    return get_request(
        route_name="filmShowTimes",
        headers=headers,
        request_cls=ShowtimesGetRequest,
        response_cls=ShowtimesGetResponse,
    )
