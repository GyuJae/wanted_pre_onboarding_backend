from rest_framework.test import APITestCase
from requests.auth import HTTPBasicAuth
from .models import Product
from users.models import User


class TestManufacturer(APITestCase):

    url = "/products/"

    # def setUp(self) -> None:
    #     User.objects.create(username="test_user", password="1", email="test@test.com")
    #     self.client.session.user = HTTPBasicAuth("test_user", "1")
    #     self.client.headers.
    #     Product.objects.create(
    #         title="test product",
    #         description="this is test product",
    #         target_amount=1000,
    #         funding_end_date="2022-04-20",
    #         one_time_funding_amount=200,
    #     )

    # def test_get_products(self):

    #     response = self.client.get(self.url)
    #     result = response.json()
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIsInstance(result, list)
    #     self.assertIsEqual(result[0]["title"], "test product")
