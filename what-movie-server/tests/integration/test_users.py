import json

from what_movie_server.app import db
from what_movie_server.schemas import UserSchema
from what_movie_server.models import User, Favourites
from tests.integration.helpers import compare_sqlalchemy_objects
from tests.integration.base import BaseTestCase


def read_user(self, email: str):
    return self.client.get(
        f"/users/{email}",
        content_type="application/json",
    )


def delete_user(self, user_id: int):
    return self.client.delete(
        f"/users/{user_id}",
        content_type="application/json",
    )


def list_users(self):
    return self.client.get(
        "/users",
        content_type="application/json",
    )


class TestUsersBlueprint(BaseTestCase):
    def test_read_user_success(self):
        """Test reading user when all ok"""
        email = "joe@gmail.com"
        user = User(email=email, password="test")
        db.session.add(user)
        db.session.commit()
        response = read_user(self, email=email)

        # check that the user in table is the same
        current_user = User.query.filter_by(email=email).first()
        expected_user = user
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "success")
        self.assertTrue(compare_sqlalchemy_objects(current_user, expected_user))
        expected_user = UserSchema.from_orm(expected_user).dict()
        expected_user["added_on"] = expected_user["added_on"].strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.assertTrue(data["data"] == expected_user)
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_read_user_not_exists(self):
        """Test reading user when it does not exist"""
        email = "joe@gmail.com"
        response = read_user(self, email=email)
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "fail")
        self.assertTrue(data["message"] == f"User does not exist: {email}")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_user_success(self):
        """Test deleting user when all ok"""
        user_id = 1
        user = User(email="joe@gmail.com", password="test")
        db.session.add(user)
        db.session.commit()
        current_user = User.query.filter_by(id=user_id).first()
        self.assertIsNotNone(current_user)
        response = delete_user(self, user_id=user_id)
        user = User.query.filter_by(id=user_id).first()
        data = json.loads(response.data.decode())
        self.assertIsNone(user)
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["message"] == f"User {user_id} deleted successfully")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_user_success_and_deletes_favourites(self):
        """Test deleting user when all ok also deletes favourites"""
        user_id = 1
        user = User(email="joe@gmail.com", password="test")
        favourite = Favourites(
            user_id=user_id, film_id=1, cinema_id=1, start_time="00:00", end_time="11:11", cinema_type="Standard"
        )
        db.session.add(user)
        db.session.add(favourite)
        db.session.commit()
        current_user = User.query.filter_by(id=user_id).first()
        self.assertIsNotNone(current_user)
        current_favourite = Favourites.query.filter_by(user_id=user_id).first()
        self.assertIsNotNone(current_favourite)
        response = delete_user(self, user_id=user_id)
        user = User.query.filter_by(id=user_id).first()
        favourite = Favourites.query.filter_by(user_id=user_id).first()
        data = json.loads(response.data.decode())
        self.assertIsNone(user)
        self.assertIsNone(favourite)
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["message"] == f"User {user_id} deleted successfully")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_user_not_exists(self):
        """Test deleting user when user does not exist"""
        user_id = 1
        response = delete_user(self, user_id=user_id)
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "fail")
        self.assertTrue(data["message"] == f"User does not exist: {user_id}")
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 404)

    def test_list_users_success_users_exist(self):
        """Test listing users when all ok"""
        user_1 = User(email="joe@gmail.com", password="test")
        user_2 = User(email="tim@gmail.com", password="test")
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()
        response = list_users(self)
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "success")
        user_1 = UserSchema.from_orm(user_1).dict()
        user_2 = UserSchema.from_orm(user_2).dict()
        user_1["added_on"] = user_1["added_on"].strftime("%a, %d %b %Y %H:%M:%S GMT")
        user_2["added_on"] = user_2["added_on"].strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.assertTrue(data["data"] == [user_1, user_2])
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)

    def test_list_favourite_success_favourites_do_not_exist(self):
        """Test listing users when no users exist"""
        response = list_users(self)
        data = json.loads(response.data.decode())
        self.assertTrue(data["status"] == "success")
        self.assertTrue(data["data"] == [])
        self.assertTrue(response.content_type == "application/json")
        self.assertEqual(response.status_code, 200)
