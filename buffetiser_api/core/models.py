"""

"""

import django
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models import Sum

from core.constants import Constants


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # Associate this model with its manager

    USERNAME_FIELD = "email"


class Investment(models.Model):
    """
    This represents either Shares or Crypto-currency. There is only one of
    these for each type:platform:symbol in the system.
    Each one however, can have multiple purchases and sales.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=8)
    investment_type = models.CharField(
        choices=Constants.InvestmentType.choices,
        max_length=16,
        default=Constants.InvestmentType.SHARES,
        null=False,
    )
    live_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.name} ({self.symbol})"

    class Meta:
        unique_together = [
            "user",
            "name",
        ]

    @property
    def all_purchases(self):
        """Get all the purchases for this investment via reverse."""

        return self.purchases.all()

    @property
    def all_sales(self):
        """Get all the sales for this investment via reverse."""

        return self.sales.all()

    @property
    def total_units_purchased(self):
        """
        The sum of all units purchased.
        """
        total_units_purchased = self.all_purchases.aggregate(Sum("units")).get(
            "units__sum"
        )

        return total_units_purchased

    @property
    def total_units_sold(self):
        """
        The sum of all units sold units.
        """
        total_units_sold = self.all_sales.aggregate(Sum("units")).get("units__sum")

        return total_units_sold

    @property
    def total_units_held(self):
        """
        The sum of all units purchased minus all units sold.
        """

        return self.total_units_purchased - self.total_units_sold

    @property
    def total_cost_excluding_fees(self) -> float:
        """
        The sum of the cost each purchase made excluding fees.
        """
        total_cost = sum(
            purchase.price_per_unit * purchase.units for purchase in self.all_purchases
        )

        return total_cost

    @property
    def total_yield_excluding_fees(self) -> float:
        """
        The sum of the income for each sale made excluding fees.
        """
        total_yield = sum(sale.price_per_unit * sale.units for sale in self.all_sales)

        return total_yield

    @property
    def total_fees(self) -> float:
        """
        The sum of the fees for each purchase.
        """
        total_fees = sum(purchase.fees for purchase in self.all_purchases)
        total_fees += sum(sale.fees for sale in self.all_sales)

        return total_fees

    @property
    def average_cost_excluding_fees(self) -> float:
        """
        The average cost over all purchases excluding fees.
        """
        return self.total_cost_excluding_fees / self.total_units_purchased

    @property
    def total_current_value(self) -> float:
        """
        The current value of all units held.
        """
        return self.total_units_held * self.live_price

    @property
    def total_profit(self) -> float:
        """
        The current value of all units held minus all costs.
        """
        return (
            self.total_current_value - self.total_cost_excluding_fees - self.total_fees
        )

    @property
    def daily_gain(self) -> float:
        """
        The profit or loss for an Investment for the current day.
        """
        # Use history
        pass

    @property
    def portfolio_daily_gain(self) -> float:
        """
        The profit or loss for an Investment for the current day.
        """
        # Use history - where does this belong?
        pass


class Purchase(models.Model):
    """
    Each purchase is related to a specific investment and provides info to its
    Investment object.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    investment = models.ForeignKey(
        to=Investment, related_name="purchases", on_delete=models.CASCADE
    )
    platform = models.CharField(
        choices=Constants.Platforms.choices,
        max_length=128,
        default=Constants.Platforms.CMC,
    )
    currency = models.CharField(max_length=5, default="AUD")
    exchange = models.CharField(
        choices=Constants.Exchanges.choices,
        max_length=4,
        default=Constants.Exchanges.XASX,
    )
    units = models.IntegerField()
    fees = models.IntegerField()
    price_per_unit = models.IntegerField()
    date_time = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        unique_together = [
            "user",
            "investment",
            "date_time",
        ]

    def __str__(self) -> str:
        return f"{self.user} purchased {self.units} {self.investment.symbol} \
            at ${self.price_per_unit}"


class Sale(models.Model):
    """
    Remove investment and update all values.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    investment = models.ForeignKey(
        to=Investment, related_name="sales", on_delete=models.CASCADE
    )
    units = models.IntegerField()
    price_per_unit = models.IntegerField()
    fees = models.IntegerField()
    date_time = models.DateField(default=django.utils.timezone.now)

    class Meta:
        unique_together = [
            "user",
            "investment",
            "date_time",
        ]

    def __str__(self) -> str:
        return f"{self.user} sold {self.units} {self.investment.symbol} at ${self.price_per_unit}"


class History(models.Model):
    """
    This will hold a lot of data about the performance of an Investment for each day.
    It will be used to supplement the investment buy/sell data and update current
    values e.g. current price.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    investment = models.ForeignKey(to=Investment, on_delete=models.CASCADE)
    date = models.DateTimeField(default=django.utils.timezone.now)
    high = models.IntegerField(default=0)
    low = models.IntegerField(default=0)
    close = models.IntegerField(default=0)
    volume = models.IntegerField(default=0)

    class Meta:
        unique_together = [
            "user",
            "investment",
            "date",
        ]

    def __str__(self) -> str:
        return f"{self.investment.symbol} - {self.date}: {self.close}"


# class Financials(Model):
#     """
#     A collection of fields and properties that represent values that span
#     the whole portfolio.
#     """

#     bank_balance = FloatField()
