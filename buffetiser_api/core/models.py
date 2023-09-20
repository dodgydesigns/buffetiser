# from datetime import datetime
# from typing import Union

# from django.db.models import (
#     Model,
#     FloatField,
#     CharField,
#     DateField,
#     DateTimeField,
#     JSONField,
#     ForeignKey,
#     CASCADE,
# )
# from config.constants import Constants


# class Investment(Model):
#     """
#     This represents either Shares or Crypto-currency. There is only one of these
#     of each type:platform:symbol in the system.
#     Each one of these however, can have multiple purchases and sales.
#     """

#     # key will be purchase/sale exchange-symbol
#     key = CharField(max_length=32, primary_key=True, default=None)
#     name = CharField(max_length=32, default=None, null=True)
#     symbol = CharField(max_length=32, default=None, null=True)
#     type = CharField(
#         choices=Constants.InvestmentType.choices,
#         max_length=16,
#         default=Constants.InvestmentType.SHARES,
#         null=False,
#     )
#     live_price = FloatField(default=0)
#     price_history = JSONField(null=True)
#     # This will include all purchases and sales as well as price history
#     value_history = JSONField(null=True)
#     # might be able to get rid of this and live draw from history
#     plot_path = CharField(
#         max_length=512, default="./"
#     )  # hold the path of the last history plot.

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


# class Purchase(Model):
#     """
#     The basis of an Investment. Most Investment details are held here.
#     """

#     investment = ForeignKey(to=Investment, on_delete=CASCADE)
#     symbol = CharField(max_length=5)

#     investment_type = CharField(
#         null=False,
#         choices=Constants.InvestmentType.choices,
#         max_length=16,
#         default=Constants.InvestmentType.SHARES,
#     )
#     investment_name = CharField(null=False, max_length=128, default="unnamed")
#     currency = CharField(max_length=5, default="AUD")
#     exchange = CharField(
#         choices=Constants.Exchanges.choices,
#         max_length=4,
#         default=Constants.Exchanges.XASX,
#     )
#     platform = CharField(
#         choices=Constants.Platforms.choices,
#         max_length=128,
#         default=Constants.Platforms.CMC,
#     )
#     units = FloatField()
#     price_per_unit = FloatField()
#     fee = FloatField()
#     date_time = DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ("exchange", "symbol", "date_time")


# class Sale(Model):
#     """
#     Remove shares and update all values.
#     """

#     investment = ForeignKey(to=Investment, on_delete=CASCADE)

#     units = FloatField()
#     price_per_unit = FloatField()
#     fee = FloatField()
#     date = DateField(auto_now=True)


# class Financials(Model):
#     """
#     A collection of fields and properties that represent values that span
#     the whole portfolio.
#     """

#     bank_balance = FloatField()
