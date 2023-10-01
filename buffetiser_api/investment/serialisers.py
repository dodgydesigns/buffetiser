"""
Serialiser for the APIs.
"""
from rest_framework import serializers

from core.models import Investment


class InvestmentSerialiser(serializers.ModelSerializer):
    """Serialiser for Investment."""

    class Meta:
        model = Investment
        fields = ["id", "name", "symbol", "investment_type", "live_price"]
        read_only_fields = ["id"]
