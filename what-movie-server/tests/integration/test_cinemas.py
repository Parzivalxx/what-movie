import json

from what_movie_server.schemas import CinemaDetailsGetRequest
from what_movie_server.app import app
from tests.integration.base import BaseTestCase


REQUEST_RETRIES = app.config["REQUEST_RETRIES"]


def get_cinemas_details(self, cinema_id: int):
    return self.client.get(
        "/cinemas/details",
        query_string=CinemaDetailsGetRequest(cinema_id=cinema_id).dict(),
        content_type="application/json",
    )


class TestCinemasBlueprint(BaseTestCase):
    def test_cinemas_details_all_valid(self):
        """Test for cinema details with valid params"""
        with self.client:
            response = get_cinemas_details(self, cinema_id=10636)
            if not response.data:
                self.assertEqual(response.status_code, 204)
            else:
                print(response.status_code)
                data = json.loads(response.data.decode())
                self.assertTrue(data["status"] == "success")
                self.assertTrue(response.content_type == "application/json")
                self.assertEqual(response.status_code, 200)

    def test_cinemas_details_invalid_cinema_id(self):
        """Test for cinema details with invalid cinema_id"""
        with self.client:
            response = get_cinemas_details(self, cinema_id=-1)
            data = json.loads(response.data.decode())
            self.assertTrue(data["status"] == "fail")
            self.assertTrue(data["message"] == f"Request timed out, attempted {REQUEST_RETRIES} times")
            self.assertEqual(response.status_code, 408)
