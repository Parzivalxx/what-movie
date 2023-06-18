from flask import request, make_response, jsonify

from what_movie_server.app import app, bcrypt, db
from what_movie_server.models import User, BlacklistToken
from what_movie_server.routes import auth_blueprint


@auth_blueprint.route("/auth/register", methods=["POST"])
def register():
    """
    User Registration Resource
    """
    # get the post data
    post_data = request.get_json()
    # check if user already exists
    user = User.query.filter_by(email=post_data.get("email")).first()
    if not user:
        try:
            user = User(
                email=post_data.get("email"), password=post_data.get("password")
            )
            # insert the user
            db.session.add(user)
            db.session.commit()
            # generate the auth token
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                "status": "success",
                "message": "Successfully registered.",
                "auth_token": auth_token,
            }
            return make_response(jsonify(response_object)), 201
        except Exception as e:
            app.logger.error(e)
            response_object = {
                "status": "fail",
                "message": "Some error occurred. Please try again.",
            }
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            "status": "fail",
            "message": "User already exists. Please Log in.",
        }
        return make_response(jsonify(response_object)), 202


@auth_blueprint.route("/auth/login", methods=["POST"])
def login():
    """
    User Login Resource
    """
    # get the post data
    post_data = request.get_json()
    try:
        # fetch the user data
        user = User.query.filter_by(email=post_data.get("email")).first()
        if user and bcrypt.check_password_hash(
            user.password, post_data.get("password")
        ):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    "status": "success",
                    "message": "Successfully logged in.",
                    "auth_token": auth_token,
                }
                return make_response(jsonify(response_object)), 200
        else:
            response_object = {"status": "fail", "message": "User does not exist."}
            return make_response(jsonify(response_object)), 404
    except Exception as e:
        app.logger.error(e)
        response_object = {"status": "fail", "message": "Try again"}
        return make_response(jsonify(response_object)), 500


@auth_blueprint.route("/auth/status", methods=["GET"])
def get_status():
    """
    User Resource
    """
    # get the auth token
    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            response_object = {
                "status": "fail",
                "message": "Bearer token malformed.",
            }
            return make_response(jsonify(response_object)), 401
    else:
        auth_token = ""
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            response_object = {
                "status": "success",
                "data": {
                    "user_id": user.id,
                    "email": user.email,
                    "admin": user.admin,
                    "registered_on": user.registered_on,
                },
            }
            return make_response(jsonify(response_object)), 200
        response_object = {"status": "fail", "message": resp}
        return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            "status": "fail",
            "message": "Provide a valid auth token.",
        }
        return make_response(jsonify(response_object)), 401


@auth_blueprint.route("/auth/logout", methods=["POST"])
def logout():
    """
    Logout Resource
    """
    # get auth token
    auth_header = request.headers.get("Authorization")
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ""
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                response_object = {
                    "status": "success",
                    "message": "Successfully logged out.",
                }
                return make_response(jsonify(response_object)), 200
            except Exception as e:
                response_object = {"status": "fail", "message": e}
                return make_response(jsonify(response_object)), 200
        else:
            response_object = {"status": "fail", "message": resp}
            return make_response(jsonify(response_object)), 401
    else:
        response_object = {
            "status": "fail",
            "message": "Provide a valid auth token.",
        }
        return make_response(jsonify(response_object)), 403
