from unittest import TestCase

from what_movie_server.app import app, db


class BaseTestCase(TestCase):
    """Base Tests"""

    def create_app(self):
        app.config.from_object("what_movie_server.config.TestingConfig")
        return app

    def setUp(self):
        self.client = self.create_app().test_client()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
