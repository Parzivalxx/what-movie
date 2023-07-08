#!/bin/bash

export APP_SETTINGS="what_movie_server.config.ProductionConfig"

# Check if .env file exists
if [ ! -f what-movie-server/what_movie_server/.env ]; then
  echo "Error: .env file not found. Please create the .env file with the required environment variables."
  exit 1
fi

# Load the environment variables from the .env file
# export $(echo $(cat what-movie-server/what_movie_server/.env | sed 's/#.*//g'| xargs) | envsubst)
export $(grep -v '^#' what-movie-server/what_movie_server/.env | xargs -d '\n')

# Check if PROD_DATABASE_URI is empty
if [ -z "$PROD_DATABASE_URI" ]; then
    echo "Error: PROD_DATABASE_URI is not set or empty."
    exit 1
fi

# Print the database URI
echo "Database URI: $PROD_DATABASE_URI"

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
flask db stamp head
flask db migrate
flask db upgrade

echo "DB migrated..."
