"""
Test importing and creating Investments from file and
exporting all Investments back to file.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from core.utils.file_utils import read_investments_from_file
from core import models


TEST_FILE = "/buffetiser_api/config/tests/sample_investment_import_file.csv"
INVESTMENTS_URL = reverse("investment:investment-list")


class TestImportExport(TestCase):
    """Test import/export Investments via file."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com", "testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_import_from_file(self):
        """Test importing from a file and creating associated Investments."""

        investment_data = read_investments_from_file(TEST_FILE)
        self.assertEqual(investment_data.status, status.HTTP_200_OK)
        self.assertEqual(len(investment_data.payload), 9)

        for symbol, investment_dict in investment_data.payload.items():
            new_investment = models.Investment.objects.create(
                user=self.user,
                symbol=symbol,
                name=investment_dict["name"],
                investment_type=investment_dict["investment_type"],
            )
            new_investment.save()

        for symbol in investment_data.payload.keys():
            self.assertIsNotNone(models.Investment.objects.filter(symbol=symbol))

    def test_create_investment_from_import(self):
        """Test that creating an Investment is successful."""

        investment_data = read_investments_from_file(TEST_FILE)
        for symbol, investment_dict in investment_data.payload.items():
            payload = {
                "investment_type": investment_dict["investment_type"],
                "name": investment_dict["name"],
                "symbol": symbol,
                "live_price": 0,
            }
            res = self.client.post(INVESTMENTS_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)

            investment = models.Investment.objects.get(id=res.data["id"])

            for key, value in payload.items():
                self.assertEqual(getattr(investment, key), value)

        self.assertEqual(investment.user, self.user)

    def test_create_investment_from_import_api(self):
        """Test that creating an Investment via the actual API is successful."""

        print("*************************************")
        # print(reverse("import"))
        print("*************************************")
