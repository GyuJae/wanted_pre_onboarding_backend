from rest_framework.test import APITestCase
from .models import Product
from users.models import User


class TestProductLists(APITestCase):

    url = "/products/"

    def setUp(self) -> None:
        self.user = User.objects.create(
            username="test_user", password="1", email="test@test.com"
        )
        self.client.force_authenticate(user=self.user)
        Product.objects.create(
            title="test product",
            description="this is test product",
            target_amount=1000,
            funding_end_date="2022-04-20",
            one_time_funding_amount=200,
            publisher=self.user,
        )
        Product.objects.create(
            title="product2",
            description="this is test product2",
            target_amount=1000,
            funding_end_date="2022-04-20",
            one_time_funding_amount=2000,
            publisher=self.user,
            total_amount=100,
        )

    def test_get_search_products(self):
        search_url = "/products/?search=test"
        response = self.client.get(search_url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "test product")
        self.assertEqual(len(result), 1)

    def test_get_order_by_created_at_products(self):
        order_by_url = "/products/?order_by=생성일"
        response = self.client.get(order_by_url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "product2")
        self.assertEqual(len(result), 2)

    def test_get_order_by_total_amount_products(self):
        order_by_url = "/products/?order_by=총펀딩금액"
        response = self.client.get(order_by_url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "product2")
        self.assertEqual(len(result), 2)

    def test_get_products(self):
        response = self.client.get(self.url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result, list)
        self.assertEqual(result[0]["title"], "test product")
        self.assertEqual(len(result), 2)

    def test_post_serializer_error_product(self):
        data = {
            "title": "new product",
            "description": "this is new product",
            "target_amount": 1000,
            "funding_end_date": "2022-04-22",
        }

        response = self.client.post(self.url, data=data, format="json")
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["one_time_funding_amount"], ["This field is required."])

    def test_post_product(self):
        data = {
            "title": "new product",
            "description": "this is new product",
            "target_amount": 1000,
            "funding_end_date": "2022-04-22",
            "one_time_funding_amount": 200,
        }

        response = self.client.post(self.url, data=data, format="json")
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["title"], "new product")


class TestProductDetail(APITestCase):

    url = "/products/1/"

    def setUp(self) -> None:
        self.user = User.objects.create(
            username="test_user", password="1", email="test@test.com"
        )
        self.client.force_authenticate(user=self.user)
        Product.objects.create(
            title="test product",
            description="this is test product",
            target_amount=1000,
            funding_end_date="2022-04-20",
            one_time_funding_amount=200,
            publisher=self.user,
        )

    def test_get_object_product(self):
        response = self.client.get(self.url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["title"], "test product")

    def test_get_object_product_error(self):
        response = self.client.get("/product/2/")

        self.assertEqual(response.status_code, 404)

    def test_get_product(self):
        response = self.client.get(self.url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["title"], "test product")

    def test_patch_not_my_product(self):

        data = {"title": "patch title"}

        another_user = User.objects.create(
            email="another@another.com", username="anothername", password="1"
        )
        self.client.force_authenticate(user=another_user)

        response = self.client.patch(self.url, data=data, format="json")
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["details"], "not your product")

    def test_patch_not_target_amount_error(self):
        data = {"target_amount": 50}

        self.client.force_authenticate(user=self.user)

        self.client.patch(self.url, data=data, format="json")

        get_response = self.client.get(self.url)
        get_result = get_response.json()

        self.assertNotEqual(data["target_amount"], get_result["target_amount"])

    def test_patch_product(self):
        data = {"title": "new title product"}

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(self.url, data=data, format="json")
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["title"], result["title"])

    def test_delete_not_my_product(self):
        another_user = User.objects.create(
            email="another@another.com", username="anothername", password="1"
        )
        self.client.force_authenticate(user=another_user)

        response = self.client.delete(self.url)
        result = response.json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["details"], "not your product")

    def test_delete_product(self):
        self.client.force_authenticate(user=self.user)

        before_products_count = Product.objects.count()
        response = self.client.delete(self.url)
        after_products_count = Product.objects.count()

        self.assertEqual(response.status_code, 204)
        self.assertNotEqual(before_products_count, after_products_count)
