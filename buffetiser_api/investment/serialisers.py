"""
Serialiser for the APIs.
"""
from rest_framework import serializers

from core.models import History, Investment, Purchase, Sale


class InvestmentSerialiser(serializers.ModelSerializer):
    """Serialiser for Investment."""

    class Meta:
        model = Investment
        fields = ["id", "name", "symbol", "investment_type", "live_price"]
        read_only_fields = ["id"]


class PurchaseSerialiser(InvestmentSerialiser):
    """Serialiser for Purchase."""

    class Meta(InvestmentSerialiser.Meta):
        model = Purchase
        fields = [
            "investment",
            "units",
            "fees",
            "price_per_unit",
            "date_time",
            "platform",
            "currency",
            "exchange",
        ]


class SaleSerialiser(InvestmentSerialiser):
    """Serialiser for Sale."""

    class Meta(InvestmentSerialiser.Meta):
        model = Sale
        fields = ["investment", "units", "fees", "price_per_unit", "date_time"]


class HistorySerialiser(InvestmentSerialiser):
    """Serialiser for History."""

    class Meta(InvestmentSerialiser.Meta):
        model = History
        fields = ["investment", "date", "open", "high", "low", "close", "volume"]
