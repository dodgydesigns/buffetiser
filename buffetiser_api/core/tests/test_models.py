"""
Tests for Models.
"""


from datetime import timedelta
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from core import models
from core.constants import Constants


def create_user(email="test@example.com", password="testpass123"):
    """Create and return a new user."""

    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test core models."""

    def test_create_user_with_email_successful(self):
        """Test successful creation of user."""

        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

        user.delete()

    def test_new_user_email_normalise(self):
        """Test that all emails (usernames) entered adhere to the rules."""

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "example_pass_123")
            self.assertEqual(user.email, expected)
            user.delete()

    def test_new_user_without_email_raises_error(self):
        """Creating a user without a valid email raises an error."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpass123")

    def test_create_superuser(self):
        """Test the creation of a superuser."""

        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "testpass123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

        user.delete()

    def test_create_investment_purchase_sale(self):
        """Test creating a new investment is successful."""

        user = get_user_model().objects.create_user(
            "test2@example.com",
            "testpass123",
        )

        investment = models.Investment.objects.create(
            user=user,
            investment_type=Constants.InvestmentType.SHARES,
            name="Megaport",
            symbol="MP1",
            live_price=2000,
        )

        purchase = models.Purchase.objects.create(
            user=user,
            investment=investment,
            platform=Constants.Platforms.CMC,
            currency="AUD",
            exchange=Constants.Exchanges.XASX,
            units=10,
            fees=5000,
            price_per_unit=5000,
        )

        purchase2 = models.Purchase.objects.create(
            user=user,
            investment=investment,
            platform=Constants.Platforms.CMC,
            currency="AUD",
            exchange=Constants.Exchanges.XASX,
            units=10,
            fees=5000,
            price_per_unit=10000,
        )

        sale = models.Sale.objects.create(
            user=user,
            investment=investment,
            units=5,
            price_per_unit=20000,
            fees=5000,
        )

        self.assertEqual(investment.user, user)
        self.assertEqual(purchase.fees, 5000)
        self.assertEqual(purchase.units, 10)
        self.assertEqual(purchase.platform, Constants.Platforms.CMC)
        self.assertEqual(purchase.exchange, Constants.Exchanges.XASX)

        self.assertEqual(purchase2.fees, 5000)
        self.assertEqual(purchase2.units, 10)
        self.assertEqual(purchase2.platform, Constants.Platforms.CMC)
        self.assertEqual(purchase2.exchange, Constants.Exchanges.XASX)

        self.assertEqual(sale.user, user)
        self.assertEqual(sale.investment, investment)
        self.assertEqual(sale.units, 5)
        self.assertEqual(sale.price_per_unit, 20000)
        self.assertEqual(sale.fees, 5000)

        self.assertEqual(investment.total_units_purchased, 20)
        self.assertEqual(investment.total_units_sold, 5)
        self.assertEqual(investment.total_units_held, 15)
        self.assertEqual(investment.total_cost_excluding_fees, 150000)
        self.assertEqual(investment.total_yield_excluding_fees, 100000)
        self.assertEqual(investment.total_fees, 15000)
        self.assertEqual(investment.average_cost_excluding_fees, 7500)
        self.assertEqual(investment.total_current_value, 30000)
        self.assertEqual(investment.total_profit, -135000)

        user.delete()

    def test_create_investment_history(self):
        """Test creating a new investment is successful."""

        date = timezone.now()
        user = get_user_model().objects.create_user(
            "test10@example.com",
            "testpass123",
        )

        investment = models.Investment.objects.create(
            user=user,
            investment_type=Constants.InvestmentType.SHARES,
            name="Megaport",
            symbol="MP1",
            live_price=2000,
        )

        models.History.objects.create(
            user=user,
            investment=investment,
            date=date,
            high=120,
            low=80,
            close=110,
            volume=10000,
        )

        models.History.objects.create(
            user=user,
            investment=investment,
            date=date + +timedelta(days=1),
            high=130,
            low=90,
            close=120,
            volume=15000,
        )

        models.History.objects.create(
            user=user,
            investment=investment,
            date=date + timedelta(days=2),
            high=140,
            low=100,
            close=130,
            volume=20000,
        )

        self.assertEqual(len(models.History.objects.filter(user=user)), 3)
        self.assertEqual(len(models.History.objects.filter(investment=investment)), 3)

        for history_entry in models.History.objects.filter(investment=investment):
            self.assertEqual(history_entry.user, user)
            self.assertEqual(history_entry.investment, investment)

        user.delete()
