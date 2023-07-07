#!/bin/sh

# Run Flask commands
flask drop_db
flask create_db
flask db migrate

# Start the Flask application
exec flask run --host=0.0.0.0