import os
import pytz
import sqlalchemy as sa
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate


app = Flask(__name__)
CORS(app, supports_credentials=True)

app_settings = os.getenv("APP_SETTINGS", "what_movie_server.config.DevelopmentConfig")
app.config.from_object(app_settings)
timezone = pytz.timezone(app.config["TIMEZONE"])

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from what_movie_server.routes.auth import auth_blueprint  # noqa
from what_movie_server.routes.movies import movies_blueprint  # noqa
from what_movie_server.routes.favourites import favourites_blueprint  # noqa
from what_movie_server.routes.users import users_blueprint  # noqa
from what_movie_server.routes.cinemas import cinemas_blueprint  # noqa
from what_movie_server.commands import register_cli_commands  # noqa

register_cli_commands(app, db)

app.register_blueprint(auth_blueprint)
app.register_blueprint(movies_blueprint)
app.register_blueprint(favourites_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(cinemas_blueprint)

if __name__ == "__main__":
    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info("Initialized the database!")
    else:
        app.logger.info("Database already contains the users table.")
    app.run()
