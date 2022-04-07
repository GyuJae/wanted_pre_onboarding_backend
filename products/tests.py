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
