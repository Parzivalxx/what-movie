from flask import Blueprint

# Create a blueprint for the data routes
data_routes = Blueprint("data", __name__)

# Import the routes to be registered
from .data import *

# Optionally, you can define any common behavior or middleware for the data routes here
# For example, you can define a before_request function that will be executed before each request

# You can also define other routes in different files and import them here to register with the blueprint
# For example, you can have separate files for different sets of routes

# Import additional routes to be registered with the blueprint
# from .other_routes import *
