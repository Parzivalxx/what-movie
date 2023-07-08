#!/bin/bash

export APP_SETTINGS="what_movie_server.config.ProductionConfig"

# Load the environment variables from the .env file
export $(grep -v '^#' ../what-movie-server/what_movie_server/.env | xargs -d '\n')

# Change directory to the project root
cd what-movie-server

# Activate the poetry environment and install dependencies
poetry shell
poetry install

cd what_movie_server

# Set the Flask app and database URI
export FLASK_APP=app.py

# Run the Flask commands
flask drop_db
flask create_db
flask db migrate

echo "DB migrated..."








