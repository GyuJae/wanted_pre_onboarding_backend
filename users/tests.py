from rest_framework.test import APITestCase
from .models import User


class TestUserList(APITestCase):

    url = "/users/"

    def setUp(self) -> None:
        User.objects.create(email="test@test.com", username="testname", password=1)

    def test_get_users(self):
        response = self.client.get(self.url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["username"], "testname")

    def test_post_users_error_already_username(self):

        data = {
            "username": "testname",
            "email": "testname@testname.com",
            "password": "1",
        }

        response = self.client.post(self.url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            result["username"], ["A user with that username already exists."]
        )

    def test_post_users(self):
        data = {
            "username": "posttest",
            "email": "postest@posttest.com",
            "password": "1",
        }

        response = self.client.post(self.url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["username"], "posttest")
        self.assertEqual(User.objects.count(), 2)


class TestUserDetail(APITestCase):
    url = "/users/1"

    def setUp(self) -> None:
        User.objects.create(email="test@test.com", username="testname", password=1)

    def test_get_user(self):
        response = self.client.get(self.url, {}, True)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["username"], "testname")

    def test_patch_user(self):

        data = {"username": "patchname"}

        response = self.client.patch(self.url, data=data, follow=True)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["username"], "patchname")
