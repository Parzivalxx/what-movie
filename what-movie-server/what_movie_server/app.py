import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate


app = Flask(__name__)
CORS(app)

app_settings = os.getenv("APP_SETTINGS", "what_movie_server.config.DevelopmentConfig")
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from what_movie_server.routes.auth import auth_blueprint
from what_movie_server.routes.movies import movies_blueprint
from what_movie_server.routes.favourites import favourites_blueprint
from what_movie_server.routes.users import users_blueprint
from what_movie_server.commands import register_cli_commands

register_cli_commands(app, db)

app.register_blueprint(auth_blueprint)
app.register_blueprint(movies_blueprint)
app.register_blueprint(favourites_blueprint)
app.register_blueprint(users_blueprint)

if __name__ == "__main__":
    app.run()
