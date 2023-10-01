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
    name = models.CharField(max_length=32)
    symbol = models.CharField(max_length=32)
    investment_type = models.CharField(
        choices=Constants.InvestmentType.choices,
        max_length=16,
        default=Constants.InvestmentType.SHARES,
        null=False,
    )
    live_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name + (self.symbol)

    @property
    def all_purchases(self):
        """Get all the purchases for this investment via reverse."""

        return self.purchases.all()

    # @property
    # def all_sales(self):
    #     """Get all the sales for this investment via reverse."""

    #     return self.sales.all()

    # unitsHeld=CALC
    # totalFees=CALC
    # averageCost=CALC
    # totalCost=CALC
    # totalValue=CALC
    # profit=CALC
    # percentProfit=CALC
    # plotPath=CALC


#     def add_purchase(self, purchase) -> None:
#         date_time = datetime.now()
#         self.price_history[str(date_time)] = purchase.price_per_unit
#         self.value_history[str(date_time)] = self.total_value + (
#             purchase.price_per_unit * purchase.units
#         )
#         self.type = purchase.investment_type
#         self.save()

#     def add_sale(self, sale) -> bool:
#         # modify bank_balance ???

#         if self.total_units < sale.units:
#             raise Exception(
#                 f"Only {self.total_units} units of {self.name} ({self.symbol}) are held."
#             )

#         date_time = datetime.now()
#         self.value_history[str(date_time)] = self.total_value - (
#             sale.price_per_unit * sale.units
#         )
#         self.save()
#         return True

#     @staticmethod
#     def generate_key(exchange, symbol):
#         return f"{exchange}-{symbol}"

#     @property
#     def total_units(self) -> Union[int, float]:
#         """
#         The sum of all units purchased minus sold units.
#         """
#         total_units = 0
#         purchases = Purchase.objects.filter(investment=self)
#         for purchase in purchases:
#             total_units += purchase.units

#         sales = Sale.objects.filter(investment=self)
#         for sale in sales:
#             total_units -= sale.units

#         if self.type == Constants.InvestmentType.SHARES:
#             return int(total_units)
#         else:
#             return total_units

#     @property
#     def total_cost_excluding_fees(self) -> float:
#         """
#         The sum of the cost each purchase made excluding fees.
#         """
#         total_cost = 0
#         purchases = Purchase.objects.filter(investment=self)
#         for purchase in purchases:
#             total_cost += purchase.price_per_unit * purchase.units

#         sales = Sale.objects.filter(investment=self)
#         for sale in sales:
#             total_cost -= sale.price_per_unit * sale.units

#         return total_cost + self.total_fees

#     @property
#     def average_cost_excluding_fees(self) -> float:
#         """
#         The sum of each purchase made.
#         """
#         return self.total_cost_excluding_fees / self.total_units

#     @property
#     def total_value(self) -> float:
#         """
#         The current value of all units held.
#         """
#         return self.total_units * self.live_price

#     @property
#     def total_fees(self) -> float:
#         """
#         The sum of the fees for each purchase.
#         """
#         total_fees = 0
#         purchases = Purchase.objects.filter(investment=self)
#         for purchase in purchases:
#             total_fees += purchase.fee

#         sales = Sale.objects.filter(investment=self)
#         for sale in sales:
#             total_fees += sale.fee

#         return total_fees

#     @property
#     def daily_gain(self) -> float:
#         """
#         The profit or loss for current day.
#         """
#         # Use history
#         pass

#     @property
#     def total_profit(self) -> float:
#         """
#         The current value of all units held minus all costs.
#         """
#         return self.total_value - self.total_cost_excluding_fees - self.total_fees


class Purchase(models.Model):
    """
    The basis of an Investment. Most Investment details are held here.
    """

    investment = models.ForeignKey(to=Investment, related_name="purchases", on_delete=models.CASCADE)

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

    def __str__(self) -> str:
        return f"Purchased {self.units} at ${self.price_per_unit}"


class Sale(models.Model):
    """
    Remove investment and update all values.
    """

    investment = models.ForeignKey(to=Investment, related_name="sales", on_delete=models.CASCADE)

    units = models.IntegerField()
    price_per_unit = models.IntegerField()
    fee = models.IntegerField()
    date = models.DateField(default=django.utils.timezone.now)

    def __str__(self) -> str:
        return f"Sold {self.units} at ${self.price_per_unit}"

# class Financials(Model):
#     """
#     A collection of fields and properties that represent values that span
#     the whole portfolio.
#     """

#     bank_balance = FloatField()
