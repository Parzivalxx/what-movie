#!/bin/bash

# Check if .env file exists
if [ ! -f what-movie-server/what_movie_server/.env ]; then
  echo "Error: .env file not found. Please create the .env file with the required environment variables."
  exit 1
fi

# Load environment variables from .env file
set -a
. what-movie-server/what_movie_server/.env
set +a

echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
echo "POSTGRES_DB: $POSTGRES_DB"
echo "SECRET_KEY: $SECRET_KEY"
echo "API_KEY: $API_KEY"
echo "AUTHORIZATION: $API_KEY"
echo "PROD_DATABASE_URI: $PROD_DATABASE_URI"

# Build the Docker images and start the containers
docker-compose up --build
