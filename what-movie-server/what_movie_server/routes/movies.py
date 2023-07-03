from flask_pydantic import validate

from what_movie_server.schemas import (
    ComingsoonGetRequest,
    ComingsoonGetResponse,
    NowshowingGetRequest,
    NowshowingGetResponse,
    ShowtimesGetRequest,
    ShowtimesGetResponse,
    DetailsGetRequest,
    DetailsGetResponse,
)
from what_movie_server.routes import movies_blueprint
from what_movie_server.routes.decorators import add_request_headers
from .helpers import get_request


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


@movies_blueprint.route("/movies/details", methods=["GET"])
@add_request_headers
@validate()
def get_movies_details(query: DetailsGetRequest, headers=None):
    """
    Retrieve the details for a selected movie
    """
    return get_request(
        route_name="filmDetails",
        headers=headers,
        params=query.dict(),
        response_cls=DetailsGetResponse,
    )
