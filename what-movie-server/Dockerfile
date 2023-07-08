# Base image
FROM python:3.7

# Set working directory
WORKDIR /app

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python -

# Copy the poetry.lock and pyproject.toml files
COPY pyproject.toml poetry.lock ./

ENV PATH="${PATH}:/root/.local/bin"

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy application files
COPY . .
RUN chmod +x /app/entrypoint.sh

# Change to the backend directory
WORKDIR /app/what_movie_server

# Expose port 5000
EXPOSE 5000

# run entrypoint
ENTRYPOINT [ "/app/entrypoint.sh" ]
