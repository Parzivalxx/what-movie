from flask import Flask
from flask_cors import CORS
from what_movie_server.routes.data import data_routes

app = Flask(__name__)
CORS(app)
app.register_blueprint(data_routes)


if __name__ == "__main__":
    app.run()
