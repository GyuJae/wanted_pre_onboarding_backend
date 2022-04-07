from rest_framework.test import APITestCase

from users.views import UserDetail
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
    url = "/users/1/"
    pk = 1
    data = {"username": "patchname"}

    def setUp(self) -> None:
        self.user = User.objects.create(
            email="test@test.com", username="testname", password="1"
        )

        self.view = UserDetail.as_view()

    def test_get_user(self):
        response = self.client.get(self.url, {}, True)
        result = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["username"], "testname")

    def test_patch_user_permissions_error(self):

        response = self.client.patch(self.url, data=self.data, follow=True)

        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result["detail"], "Authentication credentials were not provided."
        )

    def test_patch_user_no_authorization(self):

        another_user = User.objects.create(
            email="another@another.com", username="anothername", password="1"
        )
        self.client.force_authenticate(user=another_user)

        response = self.client.patch(self.url, data=self.data, follow=True)
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["errors"], "No Authorizations")

    def test_patch_user(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(self.url, data=self.data, follow=True)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["username"], self.data["username"])

    def test_delete_permissions_error(self):
        response = self.client.patch(self.url, follow=True)

        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            result["detail"], "Authentication credentials were not provided."
        )

    def test_delete_user_no_authorization(self):
        another_user = User.objects.create(
            email="another@another.com", username="anothername", password="1"
        )
        self.client.force_authenticate(user=another_user)

        response = self.client.delete(self.url, follow=True)
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["errors"], "No Authorizations")

    def test_delete_user(self):
        self.client.force_authenticate(user=self.user)
        before_delete_user_count = User.objects.all().count()
        response = self.client.delete(self.url, follow=True)
        after_delete_user_count = User.objects.all().count()
        self.assertEqual(response.status_code, 204)
        self.assertNotEqual(before_delete_user_count, after_delete_user_count)
