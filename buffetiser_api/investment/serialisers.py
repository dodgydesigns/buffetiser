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


class InvestmentImportSerialiser(serializers.Serializer):
    """
    Serializer to accept list of Investment data.

    Expect data in form:
        [
            {
            "name": "aa",
            "symbol": "a",
            "investment_type": "Shares",
            "live_price": 2147483647
            },
            {
            "name": "bb",
            "symbol": "b",
            "investment_type": "Shares",
            "live_price": 2147483647
            }
        ]
    """

    import_data = serializers.ListField(child=InvestmentSerialiser(), required=False)

    def to_internal_value(self, data):
        """Turn the list of dicts of string into nice Investment objects."""
        payload = []
        for investment_dict in data:
            investment = Investment.objects.create(
                user=self.context.get("user"),
                investment_type=investment_dict["investment_type"],
                name=investment_dict["name"],
                symbol=investment_dict["symbol"],
                live_price=0,
            )
            payload.append(investment)

        return super(InvestmentImportSerialiser, self).to_internal_value(
            {"payload": payload}
        )


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
        fields = ["investment", "date", "high", "low", "close", "volume"]
