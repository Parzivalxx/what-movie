from flask_pydantic import validate

from what_movie_server.schemas import CinemaDetailsGetRequest, CinemaDetailsGetResponse
from what_movie_server.routes import cinemas_blueprint
from what_movie_server.routes.decorators import add_request_headers
from .helpers import get_request


@cinemas_blueprint.route("/cinemas/details", methods=["GET"])
@add_request_headers
@validate()
def get_cinemas_details(query: CinemaDetailsGetRequest, headers=None):
    """
    Retrieve the details for a selected cinema
    """
    return get_request(
        route_name="cinemaDetails",
        headers=headers,
        params=query.dict(),
        response_cls=CinemaDetailsGetResponse,
    )
