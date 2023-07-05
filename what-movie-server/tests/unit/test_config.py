from flask import current_app
from unittest import TestCase

from what_movie_server.app import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object("what_movie_server.config.DevelopmentConfig")
        return app

    def test_app_is_development(self):
        # app = self.create_app().test_client()
        self.create_app()
        self.assertFalse(app.config["SECRET_KEY"] == "my_precious")
        self.assertTrue(app.config["DEBUG"])
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object("what_movie_server.config.TestingConfig")
        return app

    def test_app_is_testing(self):
        self.create_app()
        self.assertFalse(app.config["SECRET_KEY"] == "my_precious")
        self.assertTrue(app.config["DEBUG"])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object("what_movie_server.config.ProductionConfig")
        return app

    def test_app_is_production(self):
        self.create_app()
        self.assertFalse(app.config["DEBUG"])
