from flask import Blueprint

# Create a blueprint for the auth routes
auth_blueprint = Blueprint("auth", __name__)
movies_blueprint = Blueprint("movies", __name__)
favourites_blueprint = Blueprint("favourites", __name__)
users_blueprint = Blueprint("users", __name__)
cinemas_blueprint = Blueprint("cinemas", __name__)

# Import the routes to be registered
from what_movie_server.routes.auth import *  # noqa
from what_movie_server.routes.movies import *  # noqa
from what_movie_server.routes.favourites import *  # noqa
from what_movie_server.routes.users import *  # noqa
from what_movie_server.routes.cinemas import *  # noqa
