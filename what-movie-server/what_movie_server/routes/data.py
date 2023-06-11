from flask import jsonify
from . import data_routes


@data_routes.route("/api/data")
def get_data():
    data = {"message": "Hello from Flask!", "number": 42}
    return jsonify(data)
