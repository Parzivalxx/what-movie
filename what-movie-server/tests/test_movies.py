import json

from what_movie_server.app import app
from tests.base import BaseTestCase


REQUEST_RETRIES = app.config["REQUEST_RETRIES"]


def get_movies_now_showing(self, num_results: int):
    return self.client.get(
        "/movies/nowshowing",
        query_string={"n": num_results},
        content_type="application/json",
    )


def get_movies_coming_soon(self, num_results: int):
    return self.client.get(
        "/movies/comingsoon",
        query_string={"n": num_results},
        content_type="application/json",
    )


def get_movies_showtimes(self, film_id: int, date: str, num_results: int):
    return self.client.get(
        "/movies/showtimes",
        query_string={"film_id": film_id, "date": date, "n": num_results},
        content_type="application/json",
    )


class TestMoviesBlueprint(BaseTestCase):
    def test_movies_nowshowing_valid_n(self):
        """Test for now showing movies with valid number of returned results"""
        with self.client:
            response = get_movies_now_showing(self, num_results=10)
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 200)

    def test_movies_nowshowing_invalid_n(self):
        """Test for now showing movies with invalid number of returned results"""
        with self.client:
            response = get_movies_now_showing(self, num_results=-1)
            data = json.loads(response.data.decode())
            self.assertTrue(
                data["message"]
                == f"Request timed out, attempted {REQUEST_RETRIES} times"
            )
            self.assertEqual(response.status_code, 408)

    def test_movies_comingsoon_valid_n(self):
        """Test for coming soon movies with valid number of returned results"""
        with self.client:
            response = get_movies_coming_soon(self, num_results=10)
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 200)

    def test_movies_comingsoon_invalid_n(self):
        """Test for coming soon movies with invalid number of returned results"""
        with self.client:
            response = get_movies_coming_soon(self, num_results=-1)
            data = json.loads(response.data.decode())
            self.assertTrue(
                data["message"]
                == f"Request timed out, attempted {REQUEST_RETRIES} times"
            )
            self.assertEqual(response.status_code, 408)

    def test_movies_showtimes_all_valid(self):
        """Test for movie showtimes with valid params"""
        with self.client:
            response = get_movies_showtimes(
                self, film_id=25, date="2023-01-01", num_results=10
            )
            self.assertTrue(response.content_type == "application/json")
            self.assertEqual(response.status_code, 204)

    def test_movies_showtimes_invalid_film_id(self):
        """Test for movie showtimes with invalid film_id"""
        with self.client:
            response = get_movies_showtimes(
                self, film_id=-1, date="2023-01-01", num_results=10
            )
            data = json.loads(response.data.decode())
            self.assertTrue(
                data["message"]
                == f"Request timed out, attempted {REQUEST_RETRIES} times"
            )
            self.assertEqual(response.status_code, 408)

    def test_movies_comingsoon_invalid_date(self):
        """Test for movie showtimes with invalid date"""
        with self.client:
            response = get_movies_showtimes(self, film_id=25, date="a", num_results=10)
            data = json.loads(response.data.decode())
            self.assertTrue(
                data["message"]
                == f"Request timed out, attempted {REQUEST_RETRIES} times"
            )
            self.assertEqual(response.status_code, 408)

    def test_movies_comingsoon_invalid_n(self):
        """Test for movie showtimes with invalid n"""
        with self.client:
            response = get_movies_showtimes(
                self, film_id=25, date="2023-01-01", num_results=-1
            )
            data = json.loads(response.data.decode())
            self.assertTrue(
                data["message"]
                == f"Request timed out, attempted {REQUEST_RETRIES} times"
            )
            self.assertEqual(response.status_code, 408)
