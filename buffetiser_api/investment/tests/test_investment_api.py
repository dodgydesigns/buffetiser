"""
Tests for Investment API.
"""

from datetime import timedelta
import random
import string
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status
from core import models
from core.utils.net_utils import update_history
from investment.serialisers import (
    InvestmentSerialiser,
)

from config.constants import Constants

INVESTMENTS_URL = reverse("investment:investment-list")


def create_investment(user, **params):
    """Create and return a sample investment."""

    defaults = {
        "investment_type": Constants.InvestmentType.SHARES,
        "name": "".join(random.choices(string.ascii_letters, k=10)),
        "symbol": "".join(random.choices(string.ascii_uppercase, k=3)),
        "live_price": 1,
    }
    defaults.update(params)
    investment = models.Investment.objects.create(user=user, **defaults)

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
    purchase = models.Purchase.objects.create(
        user=user, investment=investment, **defaults
    )

    return purchase


def create_sale(user, investment, **params):
    """Create and return a sample investment sale."""

    defaults = {
        "units": 1,
        "price_per_unit": 1,
        "fees": 1,
    }
    defaults.update(params)

    sale = models.Sale.objects.create(user=user, investment=investment, **defaults)

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
            "test@example.com", "testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_investments(self):
        """Get a list of investments."""

        create_investment(user=self.user)
        create_investment(user=self.user)

        res = self.client.get(INVESTMENTS_URL)

        investments = models.Investment.objects.all()
        serialiser = InvestmentSerialiser(investments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialiser.data)

    def test_investment_list_limited_to_user(self):
        """Test getting a list of investments that is limited to the authenticated user"""

        other_user = get_user_model().objects.create_user(
            "test2@example.com", "testpass123"
        )

        create_investment(user=other_user)
        create_investment(user=self.user)

        res = self.client.get(INVESTMENTS_URL)

        investments = models.Investment.objects.filter(user=self.user)
        serialiser = InvestmentSerialiser(investments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serialiser.data)

    def test_create_investment(self):
        """Test that creating an Investment via the actual API is successful."""

        payload = {
            "investment_type": Constants.InvestmentType.SHARES,
            "name": "Megaport",
            "symbol": "MP1",
            "live_price": 1,
        }
        res = self.client.post(INVESTMENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        investment = models.Investment.objects.get(id=res.data["id"])

        for key, value in payload.items():
            self.assertEqual(getattr(investment, key), value)

        self.assertEqual(investment.user, self.user)

    def test_create_investment_history(self):
        """Test that creating an History for an Investment."""

        payload = {
            "investment_type": Constants.InvestmentType.SHARES,
            "name": "Megaport",
            "symbol": "MP1",
            "live_price": 1,
        }
        res = self.client.post(INVESTMENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        investment = models.Investment.objects.get(id=res.data["id"])
        history_entry = models.History.objects.create(
            user=investment.user,
            investment=investment,
            date=timezone.now() - timedelta(days=1),
            high=1678,
            low=1545,
            close=1660,
            volume=109897,
        )
        history_entry.save()

        # Test that there are 2 history objects that have different values
        msg = update_history(investment)
