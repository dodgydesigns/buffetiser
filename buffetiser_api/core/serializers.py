from core.models import (DailyChange, DividendPayment, DividendReinvestment,
                         History, Investment, Purchase, Sale)
from rest_framework import serializers


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale


class DividendReinvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DividendReinvestment


class DividendPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DividendPayment


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History


class DailyChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyChange
