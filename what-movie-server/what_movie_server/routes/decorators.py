from functools import wraps
from datetime import datetime

from what_movie_server.app import app


def add_request_headers(func):
    default_headers = {
        "client": "NIL_3",
        "x-api-key": app.config["API_KEY"],
        "territory": "XX",
        "api-version": "v200",
        "geolocation": "-22.0;14.0",
        "device-datetime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "Authorization": "Basic TklMXzNfWFg6aFVwU2RVbU81eW12",
        "User-Agent": "Chrome v22.2 Linux Ubuntu",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = default_headers.copy()
        headers.update(kwargs.get("headers", {}))
        kwargs["headers"] = headers
        return func(*args, **kwargs)

    return wrapper
