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

# Build the Docker images and start the containers
docker-compose up --build
