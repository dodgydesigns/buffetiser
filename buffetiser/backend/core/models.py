from typing import Union

from core.config import Constants
from django.db.models import (CASCADE, CharField, DateField, FloatField,
                              ForeignKey, IntegerField, Model, BooleanField)


def date_to_string(date):
    """Ensure all dates are formatted the same."""
    return date.strftime("%d/%m/%Y")


class Investment(Model):
    """
    This represents either Shares or Crypto-currency. There is only one of these
    of each type:platform:symbol in the system.
    Each one of these however, can have multiple purchases and sales.
    """

    key = CharField(max_length=32, primary_key=True, default=None)
    name = CharField(max_length=128, default=None, null=True)
    symbol = CharField(max_length=32, default=None, null=True)
    type = CharField(
        choices=Constants.InvestmentType.choices,
        max_length=16,
        default=Constants.InvestmentType.SHARES,
        null=False,
    )
    live_price = FloatField(default=0)
    visible = BooleanField(default=True)

    @staticmethod
    def generate_key(exchange, symbol):
        return f"{exchange}-{symbol}"

    @property
    def total_units(self) -> Union[int, float]:
        """
        The sum of all units purchased minus sold units.
        """
        total_units = 0
        purchases = Purchase.objects.filter(investment=self)
        for purchase in purchases:
            total_units += purchase.units

        sales = Sale.objects.filter(investment=self)
        for sale in sales:
            total_units -= sale.units

        if self.type == Constants.InvestmentType.SHARES:
            return int(total_units)
        else:
            return total_units

    @property
    def total_cost_excluding_fees(self) -> float:
        """
        The sum of the cost each purchase made excluding fees.
        """
        total_cost = 0
        purchases = Purchase.objects.filter(investment=self)
        for purchase in purchases:
            total_cost += purchase.price_per_unit * purchase.units

        sales = Sale.objects.filter(investment=self)
        for sale in sales:
            total_cost -= sale.price_per_unit * sale.units

        return total_cost + self.total_fees

    @property
    def average_cost_excluding_fees(self) -> float:
        """
        The sum of each purchase made.
        """
        return self.total_cost_excluding_fees / self.total_units

    @property
    def total_value(self) -> float:
        """
        The current value of all units held.
        """
        return self.total_units * self.live_price

    @property
    def total_fees(self) -> float:
        """
        The sum of the fees for each purchase.
        """
        total_fees = 0
        purchases = Purchase.objects.filter(investment=self)
        for purchase in purchases:
            total_fees += purchase.fee

        sales = Sale.objects.filter(investment=self)
        for sale in sales:
            total_fees += sale.fee

        return total_fees

    @property
    def daily_gain(self) -> float:
        """
        The profit or loss for current day.
        """
        # Use history
        pass

    @property
    def total_profit(self) -> float:
        """
        The current value of all units held minus all costs.
        """
        return self.total_value - self.total_cost_excluding_fees - self.total_fees


class Purchase(Model):
    """
    The basis of an Investment. Most Investment details are held here.
    """

    investment = ForeignKey(to=Investment, on_delete=CASCADE)
    currency = CharField(max_length=5, default="AUD")
    exchange = CharField(
        choices=Constants.Exchanges.choices,
        max_length=4,
        default=Constants.Exchanges.XASX,
    )
    platform = CharField(
        choices=Constants.Platforms.choices,
        max_length=128,
        default=Constants.Platforms.CMC,
    )
    units = FloatField()
    price_per_unit = FloatField()
    fee = FloatField()
    date = DateField()
    trade_count = IntegerField()

    def to_json(self):
        return {
            "symbol": self.investment.symbol,
            "currency": self.currency,
            "exchange": self.exchange,
            "platform": self.platform,
            "units": self.units,
            "price_per_unit": self.price_per_unit,
            "fee": self.fee,
            "date": date_to_string(self.date),
        }

    def __str__(self):
        return f"{self.investment.symbol}: {self.units} units @ ${self.price_per_unit} with ${self.fee} fee on {self.date}"

    class Meta:
        unique_together = ("date", "trade_count", "investment")


class Sale(Model):
    """
    Remove shares and update all values.
    """

    investment = ForeignKey(to=Investment, on_delete=CASCADE)
    currency = CharField(max_length=5, default="AUD")
    exchange = CharField(
        choices=Constants.Exchanges.choices,
        max_length=4,
        default=Constants.Exchanges.XASX,
    )
    units = FloatField()
    price_per_unit = FloatField()
    fee = FloatField()
    date = DateField()
    trade_count = IntegerField()

    def to_json(self):
        return {
            "symbol": self.investment.symbol,
            "currency": self.currency,
            "exchange": self.exchange,
            "units": self.units,
            "price_per_unit": self.price_per_unit,
            "fee": self.fee,
            "date": date_to_string(self.date),
        }

    class Meta:
        unique_together = ("date", "trade_count", "investment")


class DividendReinvestment(Model):
    """
    This holds the details of a dividend that was reinvested into the portfolio.
    Reinvestment is made up of the cutoff date, the value of the Investment on that date
    and the number of shares (Investment.units) obtained.
    """

    investment = ForeignKey(to=Investment, on_delete=CASCADE)
    reinvestment_date = DateField()
    units = IntegerField(default=0)
    price_per_unit = FloatField()

    def to_json(self):
        return {
            "units": self.units,
            "reinvestment_date": date_to_string(self.reinvestment_date),
        }

    def __str__(self):
        return f"{self.investment.symbol}, {self.units} units on {self.reinvestment_date}"

    class Meta:
        unique_together = ("reinvestment_date", "investment")


class DividendPayment(Model):
    """
    If an Investment doesn't provide reinvestment or the dividend is insufficient to buy
    1 or more shares, the dividend is paid out.
    Payment is made up of the cutoff date, payment date and the value of money paid.
    """

    payment_date = DateField()
    value = FloatField()

    investment = ForeignKey(to=Investment, on_delete=CASCADE)

    def to_json(self):
        return {
            "value": self.value,
            "payment_date": date_to_string(self.payment_date),
        }

    def __str__(self):
        return f"{self.investment.key}"

    class Meta:
        unique_together = ("payment_date", "investment")


class History(Model):
    """
    This will record the daily value of an Investment per share.
    """

    date = DateField()
    high = FloatField(default=0)
    low = FloatField(default=0)
    close = FloatField(default=0)
    volume = IntegerField(default=0)

    investment = ForeignKey(to=Investment, on_delete=CASCADE)

    def __str__(self):
        return f"{self.investment.symbol, self.high, self.low, self.close}"

    class Meta:
        unique_together = ("date", "investment")


class DailyChange(Model):
    """
    We need a place to hold the most up-to-date values of each investment. Although only
    a temporary value, it should be held to provide the information on first start and
    restart of the app.
    """

    symbol = CharField(default="")
    daily_change = FloatField(default=0)
    daily_change_percent = FloatField(default=0)

    def __str__(self):
        return f"{self.symbol, self.daily_change, self.daily_change_percent}"


class Configuration(Model):
    """
    Hold any config values set by the user.
    """

    update_time = CharField(default="15:00")
    update_time_zone = CharField(default="Australia/Perth")
