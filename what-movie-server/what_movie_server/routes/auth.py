from flask import request, make_response
from flask_pydantic import validate

from what_movie_server.app import app, bcrypt, db
from what_movie_server.models import (
    User,
    BlacklistToken,
)
from what_movie_server.schemas import (
    AuthErrorResponse,
    GetstatusGetHeaders,
    GetstatusSuccessGetResponse,
    LoginPostRequest,
    LoginSuccessPostResponse,
    LogoutPostHeaders,
    LogoutSuccessPostResponse,
    RegisterPostRequest,
    RegisterSuccessPostResponse,
)
from what_movie_server.routes import auth_blueprint


@auth_blueprint.route("/auth/register", methods=["POST"])
@validate()
def register(body: RegisterPostRequest):
    """
    User Registration Resource
    """
    # check if user already exists
    user = User.query.filter_by(email=body.email).first()
    if not user:
        try:
            user = User(email=body.email, password=body.password)
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
            return (
                make_response(RegisterSuccessPostResponse.parse_obj(response_object).dict()),
                201,
            )
        except Exception as e:
            app.logger.error(e)
            response_object = {
                "status": "fail",
                "message": "Some error occurred. Please try again.",
            }
            return (
                make_response(AuthErrorResponse.parse_obj(response_object).dict()),
                401,
            )
    else:
        response_object = {
            "status": "fail",
            "message": "User already exists. Please Log in.",
        }
        return (
            make_response(AuthErrorResponse.parse_obj(response_object).dict()),
            409,
        )


@auth_blueprint.route("/auth/login", methods=["POST"])
@validate()
def login(body: LoginPostRequest):
    """
    User Login Resource
    """
    try:
        # fetch the user data
        user = User.query.filter_by(email=body.email).first()
        if user and bcrypt.check_password_hash(user.password, body.password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    "status": "success",
                    "message": "Successfully logged in.",
                    "auth_token": auth_token,
                }
                return (
                    make_response(LoginSuccessPostResponse.parse_obj(response_object).dict()),
                    200,
                )
        else:
            response_object = {"status": "fail", "message": "User does not exist."}
            return (
                make_response(AuthErrorResponse.parse_obj(response_object).dict()),
                404,
            )
    except Exception as e:
        app.logger.error(e)
        response_object = {"status": "fail", "message": "Try again"}
        return (
            make_response(AuthErrorResponse.parse_obj(response_object).dict()),
            500,
        )


@auth_blueprint.route("/auth/status", methods=["GET"])
def get_status():
    """
    User Resource
    """
    # get the auth token
    auth_header = GetstatusGetHeaders(**request.headers).Authorization
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            response_object = {
                "status": "fail",
                "message": "Bearer token malformed.",
            }
            return (
                make_response(AuthErrorResponse.parse_obj(response_object).dict()),
                401,
            )
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
                    "added_on": user.added_on,
                },
            }
            return (
                make_response(GetstatusSuccessGetResponse.parse_obj(response_object).dict()),
                200,
            )
        response_object = {"status": "fail", "message": resp}
        return (
            make_response(AuthErrorResponse.parse_obj(response_object).dict()),
            401,
        )
    else:
        response_object = {
            "status": "fail",
            "message": "Provide a valid auth token.",
        }
        return (
            make_response(AuthErrorResponse.parse_obj(response_object).dict()),
            401,
        )


@auth_blueprint.route("/auth/logout", methods=["POST"])
def logout():
    """
    Logout Resource
    """
    # get auth token
    auth_header = LogoutPostHeaders(**request.headers).Authorization
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
                return (
                    make_response(LogoutSuccessPostResponse.parse_obj(response_object).dict()),
                    200,
                )
            except Exception as e:
                response_object = {"status": "fail", "message": e}
                return (
                    make_response(AuthErrorResponse.parse_obj(response_object).dict()),
                    200,
                )
        else:
            response_object = {"status": "fail", "message": resp}
            return (
                make_response(AuthErrorResponse.parse_obj(response_object).dict()),
                401,
            )
    else:
        response_object = {
            "status": "fail",
            "message": "Provide a valid auth token.",
        }
        return (
            make_response(AuthErrorResponse.parse_obj(response_object).dict()),
            403,
        )
