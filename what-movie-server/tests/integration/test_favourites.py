import json

from what_movie_server.app import app, db
from what_movie_server.schemas import (
    CreatePayloadPostRequest,
    UpdatePayloadPutRequest,
    ListGetRequest,
    Favourite,
)
from what_movie_server.models import User, Favourites
from tests.integration.base import BaseTestCase


REQUEST_RETRIES = app.config["REQUEST_RETRIES"]


def create_favourite(
    self,
    user_id: int,
    film_id: int,
    cinema_id: int,
    start_time: str,
    end_time: int,
    is_3d: bool,
):
    return self.client.post(
        "/favourites",
        data=json.dumps(
            CreatePayloadPostRequest(
                user_id=user_id,
                film_id=film_id,
                cinema_id=cinema_id,
                start_time=start_time,
                end_time=end_time,
                is_3d=is_3d,
            ).dict()
        ),
        content_type="application/json",
    )


def read_favourite(self, favourite_id: int):
    return self.client.get(
        f"/favourites/{favourite_id}",
        content_type="application/json",
    )


def update_favourite(
    self,
    favourite_id: int,
    user_id: int,
    film_id: int,
    cinema_id: int,
    start_time: str,
    end_time: int,
    is_3d: bool,
):
    return self.client.put(
        f"/favourites/{favourite_id}",
        data=json.dumps(
            UpdatePayloadPutRequest(
                user_id=user_id,
                film_id=film_id,
                cinema_id=cinema_id,
                start_time=start_time,
                end_time=end_time,
                is_3d=is_3d,
            ).dict()
        ),
        content_type="application/json",
    )


def delete_favourite(self, favourite_id: int):
    return self.client.delete(
        f"/favourites/{favourite_id}",
        content_type="application/json",
    )


def list_favourites(self, user_id: int):
    return self.client.get(
        "/favourites",
        query_string=ListGetRequest(user_id=user_id).dict(),
        content_type="application/json",
    )


def compare_sqlalchemy_objects(object1, object2):
    # Get the attribute names of the instances
    attributes = object1.__table__.columns.keys()

    # Compare the attribute values
    for attr in attributes:
        if attr != "id":
            if getattr(object1, attr) != getattr(object2, attr):
                return False
    return True


class TestFavouritesBlueprint(BaseTestCase):
    def test_create_favourite_success(self):
        """Test creating favourites when all ok"""
        user = User(email="joe@gmail.com", password="test")
        db.session.add(user)
        db.session.commit()
        response = create_favourite(
            self,
            user_id=1,
            film_id=1,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        current_favourite = Favourites.query.filter_by(user_id=1).first()
        expected_favourite = Favourites(
            user_id=1,
            film_id=1,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(
            compare_sqlalchemy_objects(current_favourite, expected_favourite)
        )
        self.assertTrue(response.content_type == "application/json")
        self.assertTrue(data["status"] == "success")
        self.assertTrue(
            data["message"] == f"Favourite {current_favourite.id} added successfully"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_favourite_no_user(self):
        """Test creating favourites when user does not exist"""
        response = create_favourite(
            self,
            user_id=1,
            film_id=1,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "fail")
        self.assertTrue(data["message"] == "User does not exist.")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 404)

    def test_create_favourite_favourite_already_exists(self):
        """Test creating favourites when favourite already exists"""
        user = User(email="joe@gmail.com", password="test")
        favourite = Favourites(
            user_id=1,
            film_id=1,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        db.session.add(user)
        db.session.add(favourite)
        db.session.commit()
        response = create_favourite(
            self,
            user_id=1,
            film_id=1,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        existing_favourite = Favourites.query.filter_by(user_id=1).first()
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "fail")
        self.assertTrue(
            data["message"] == f"This favourite already exists: {existing_favourite.id}"
        )
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 409)

    def test_read_favourite_success(self):
        """Test reading favourites when all ok"""
        user = User(email="joe@gmail.com", password="test")
        favourite = Favourites(
            user_id=1,
            film_id=1,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        db.session.add(user)
        db.session.add(favourite)
        db.session.commit()
        response = read_favourite(self, favourite_id=1)

        # check that the favourite in table is the same
        current_favourite = Favourites.query.filter_by(id=1).first()
        expected_favourite = favourite

        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "success")
        self.assertTrue(
            compare_sqlalchemy_objects(current_favourite, expected_favourite)
        )
        self.assertTrue(data["data"] == Favourite.from_orm(current_favourite).dict())
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_read_favourite_not_exists(self):
        """Test reading favourites when it does not exist"""
        favourite_id = 1
        response = read_favourite(self, favourite_id=favourite_id)
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "fail")
        self.assertTrue(data["message"] == f"Favourite does not exist: {favourite_id}")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 404)

    def test_update_favourite_success(self):
        """Test updating favourites when all ok"""
        user = User(email="joe@gmail.com", password="test")
        favourite = Favourites(
            user_id=1,
            film_id=1,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        db.session.add(user)
        db.session.add(favourite)
        db.session.commit()
        response = update_favourite(
            self,
            favourite_id=1,
            user_id=1,
            film_id=2,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )

        # check that the favourite actually updated in the table
        current_favourite = Favourites.query.filter_by(user_id=1).first()
        expected_favourite = Favourites(
            user_id=1,
            film_id=2,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )

        data = json.loads(response.data.decode())
        self.assertTrue(
            compare_sqlalchemy_objects(current_favourite, expected_favourite)
        )
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["data"] == Favourite.from_orm(current_favourite).dict())
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_favourite_not_exists(self):
        """Test updating favourites when favourite does not exist"""
        favourite_id = 1
        response = update_favourite(
            self,
            favourite_id=favourite_id,
            user_id=1,
            film_id=2,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "fail")
        self.assertTrue(data["message"] == f"Favourite does not exist: {favourite_id}")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_favourite_success(self):
        """Test deleting favourites when all ok"""
        favourite_id = 1
        user = User(email="joe@gmail.com", password="test")
        favourite = Favourites(
            user_id=1,
            film_id=1,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        db.session.add(user)
        db.session.add(favourite)
        db.session.commit()
        current_favourite = Favourites.query.filter_by(id=favourite_id).first()
        self.assertIsNotNone(current_favourite)
        response = delete_favourite(self, favourite_id=favourite_id)
        favourite = Favourites.query.filter_by(id=favourite_id).first()
        data = json.loads(response.data.decode())
        self.assertIsNone(favourite)
        self.assertTrue(data["status"] == "success")
        self.assertTrue(
            data["message"] == f"Favourite {favourite_id} deleted successfully"
        )
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_favourite_not_exists(self):
        """Test deleting favourites when favourite does not exist"""
        favourite_id = 1
        response = delete_favourite(self, favourite_id=favourite_id)
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "fail")
        self.assertTrue(data["message"] == f"Favourite does not exist: {favourite_id}")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 404)

    def test_list_favourite_success_favourites_exist(self):
        """Test listing favourites when all ok"""
        user = User(email="joe@gmail.com", password="test")
        favourite_1 = Favourites(
            user_id=1,
            film_id=1,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        favourite_2 = Favourites(
            user_id=1,
            film_id=2,
            cinema_id=1,
            start_time="00:00",
            end_time="11:11",
            is_3d=False,
        )
        db.session.add(user)
        db.session.add(favourite_1)
        db.session.add(favourite_2)
        db.session.commit()
        response = list_favourites(self, user_id=1)
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "success")
        self.assertTrue(
            data["data"]
            == [
                Favourite.from_orm(favourite_1).dict(),
                Favourite.from_orm(favourite_2).dict(),
            ]
        )
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_list_favourite_success_favourites_do_not_exist(self):
        """Test listing favourites when no favourites exist"""
        user = User(email="joe@gmail.com", password="test")
        db.session.add(user)
        db.session.commit()
        response = list_favourites(self, user_id=1)
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["data"] == [])
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)
