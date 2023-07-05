import os
from dotenv import load_dotenv

environment = os.getenv("ENVIRONMENT", "dev")
if environment == "dev":
    load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = f"postgresql://{db_user}:{db_password}@localhost/"
database_name = "movie_showtimes"


class BaseConfig:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    API_KEY = os.getenv("API_KEY", "")
    AUTHORIZATION = os.getenv("AUTHORIZATION", "")
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    REQUEST_RETRIES = 3
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_MOVIEGLU_URL = "https://api-gate2.movieglu.com/"
    TOKEN_EXPIRATION_TIME = 30 * 60 * 60 * 24
    TIMEZONE = "UTC"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = f"{postgres_local_base}{database_name}"


class TestingConfig(BaseConfig):
    """Testing configuration."""

    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = f"{postgres_local_base}{database_name}"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TOKEN_EXPIRATION_TIME = 5


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SECRET_KEY = "my_precious"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql:///example"
