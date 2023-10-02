"""
Tests for Investment API.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from investment.serialisers import InvestmentSerialiser, PurchaseSerialiser, SaleSerialiser

from core.models import Investment, Purchase, Sale  # , Purchase, Sale
from config.constants import Constants

INVESTMENTS_URL = reverse("investment:investment-list")


def purchase_url(investment_id):
    """Create and return an Investment Purchase URL."""

    return reverse("investment:purchase-detail", args=[investment_id])


def sale_url(investment_id):
    """Create and return an Investment Sale URL."""

    return reverse("investment:sale-detail", args=[investment_id])


def create_investment(user, **params):
    """Create and return a sample investment."""

    defaults = {
        "investment_type": Constants.InvestmentType.SHARES,
        "name": "SampleShare",
        "symbol": "SSH",
        "live_price": 1,
    }
    defaults.update(params)
    investment = Investment.objects.create(user=user, **defaults)

    return investment


def create_purchase(user, investment, **params):
    """Create and return a sample purchase"""

    defaults = {
        "platform": Constants.Platforms.CMC,
        "currency": "AUD",
        "exchange": Constants.Exchanges.XASX,
        "units": 1,
        "fees": 1,
        "price_per_unit": 1,
    }
    defaults.update(params)
    purchase = Purchase.objects.create(user=user, investment=investment, **defaults)

    return purchase


def create_sale(user, investment, **params):
    """Create and return a sample investment sale."""

    defaults = {
        "units":  1,
        "price_per_unit": 1,
        "fees": 1,
    }
    defaults.update(params)

    sale = Sale.objects.create(user=user, investment=investment, **defaults)

    return sale


class PublicInvestmentAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Ensure that auth is required to call API."""

        res = self.client.get(INVESTMENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateInvestmentAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_investments(self):
        """Get a list of investments."""

        create_investment(user=self.user)
        create_investment(user=self.user)

        res = self.client.get(INVESTMENTS_URL)

        investments = Investment.objects.all().order_by("name")
        serialiser = InvestmentSerialiser(investments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serialiser.data)
        print(serialiser)

    def test_investment_list_limited_to_user(self):
        """Test getting a list of investments that is limited to the authenticated user"""

        other_user = get_user_model().objects.create_user(
            "test2@example.com",
            "testpass123"
        )

        create_investment(user=other_user)
        create_investment(user=self.user)

        res = self.client.get(INVESTMENTS_URL)

        investments = Investment.objects.filter(user=self.user)
        serialiser = InvestmentSerialiser(investments)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serialiser.data)
        print(serialiser)

    def test_get_investment_purchase(self):
        """Test getting a Purchase of an Investment."""

        investment = create_investment(user=self.user)
        purchase = create_purchase(user=self.user, investment=investment)
        purchase2 = create_purchase(user=self.user, investment=investment)

        url = purchase_url(investment.id)
        res = self.client.get(url)

        serialiser = PurchaseSerialiser(investment)
        # self.assertEqual(res.data, serialiser.data)
        print("----------------------------------------------------")
        print("serialiser", serialiser)
        print("res", res)
        print("res.data", res)
        print("purchase", purchase)
        print("purchase2", purchase2)
        print("----------------------------------------------------")

    def test_get_investment_sale(self):
        """Test getting a Sale of an Investment."""

        investment = create_investment(user=self.user)
        sale = create_sale(user=self.user, investment=investment)
        sale2 = create_sale(user=self.user, investment=investment)

        url = sale_url(investment.id)
        res = self.client.get(url)

        serialiser = SaleSerialiser(investment, many=True)
        # self.assertEqual(res.data, serialiser.data)
        print("----------------------------------------------------")
        print("serialiser", serialiser)
        print("res", res)
        print("res.data", res)
        print("sale", sale)
        print("sale2", sale2)
        print("----------------------------------------------------")