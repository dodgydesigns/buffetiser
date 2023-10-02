"""
Tests for Models.
"""


from unittest import TestCase
from django.contrib.auth import get_user_model

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

    def test_create_investment_via_purchase(self):
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
        self.assertEqual(purchase.investment.name, "Megaport")
        self.assertEqual(purchase2.investment.name, "Megaport")
        self.assertEqual(sale.investment.name, "Megaport")

        # self.assertEqual(investment.total_units_purchased, 20)
        # self.assertEqual(investment.total_units_sold, 5)
        # self.assertEqual(investment.total_units_held, 15)
        # self.assertEqual(investment.total_cost_excluding_fees, 150000)
        # self.assertEqual(investment.total_yield_excluding_fees, 100000)
        # self.assertEqual(investment.total_fees, 15000)
        # self.assertEqual(investment.average_cost_excluding_fees, 7500)
        # self.assertEqual(investment.total_current_value, 30000)
        # self.assertEqual(investment.total_profit, -135000)

        # print("-------------------------------------------")
        # print("total_units", investment.total_units_held)
        # print("total_cost_excluding_fees", investment.total_cost_excluding_fees)
        # print("total_fees", investment.total_fees)
        # print("average_cost_excluding_fees", investment.average_cost_excluding_fees)
        # print("total_value", investment.total_current_value)
        # print("total_profit", investment.total_profit)
        # print("-------------------------------------------")

    # def test_create_purchase(self):
    #     """Test creating a purchase is successful."""

    #     user = create_user()
    #     purchase =