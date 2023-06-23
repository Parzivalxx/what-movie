from flask import make_response, request
from flask_pydantic import validate
from http import HTTPStatus
import requests

from what_movie_server.schemas import (
    ComingsoonGetRequest,
    ComingsoonGetResponse,
    MoviesErrorResponse,
    NowshowingGetRequest,
    NowshowingGetResponse,
    ShowtimesGetRequest,
    ShowtimesGetResponse,
)
from what_movie_server.routes import movies_blueprint
from what_movie_server.routes.decorators import add_request_headers
from what_movie_server.app import app


BASE_MOVIEGLU_URL = app.config["BASE_MOVIEGLU_URL"]
REQUEST_RETRIES = app.config["REQUEST_RETRIES"]


def get_request(headers, route_name, params, response_cls):
    """Helper function to perform get request to MovieGlu API"""
    for _ in range(REQUEST_RETRIES):
        try:
            response = requests.get(
                f"{BASE_MOVIEGLU_URL}{route_name}/",
                params=params,
                headers=headers,
            )
            status_code = response.status_code
            if status_code == HTTPStatus.OK:
                response_object = {
                    "status": "success",
                    "data": response.json(),
                }
                return (
                    make_response(response_cls.parse_obj(response_object).dict()),
                    200,
                )
            elif status_code == HTTPStatus.NO_CONTENT:
                response_object = {
                    "status": "success",
                    "data": None,
                }
                return (
                    make_response(response_cls.parse_obj(response_object).dict()),
                    204,
                )
            else:
                app.logger.warning(f"Unaccepted status code received: {status_code}")
                continue
        except Exception as e:
            app.logger.error(e, exc_info=True)
            continue
    app.logger.error("Request run time error")
    response_object = {
        "status": "fail",
        "message": f"Request timed out, attempted {REQUEST_RETRIES} times",
    }
    return make_response(MoviesErrorResponse.parse_obj(response_object).dict()), 408


@movies_blueprint.route("/movies/nowshowing", methods=["GET"])
@add_request_headers
@validate()
def get_movies_now_showing(query: NowshowingGetRequest, headers=None):
    """
    Retrieve the currently showing movies
    """
    return get_request(
        route_name="filmsNowShowing",
        headers=headers,
        params=query.dict(),
        response_cls=NowshowingGetResponse,
    )


@movies_blueprint.route("/movies/comingsoon", methods=["GET"])
@add_request_headers
@validate()
def get_movies_coming_soon(query: ComingsoonGetRequest, headers=None):
    """
    Retrieve the movies coming soon
    """
    return get_request(
        route_name="filmsComingSoon",
        headers=headers,
        params=query.dict(),
        response_cls=ComingsoonGetResponse,
    )


@movies_blueprint.route("/movies/showtimes", methods=["GET"])
@add_request_headers
@validate()
def get_movies_showtimes(query: ShowtimesGetRequest, headers=None):
    """
    Retrieve the showtimes for a selected movie and date
    """
    return get_request(
        route_name="filmShowTimes",
        headers=headers,
        params=query.dict(),
        response_cls=ShowtimesGetResponse,
    )
