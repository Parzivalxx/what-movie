from flask import make_response
from http import HTTPStatus
import requests

from what_movie_server.schemas import ErrorResponse
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
    return make_response(ErrorResponse.parse_obj(response_object).dict()), 408
