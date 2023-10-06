"""
Views for the Investment APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import History, Investment, Purchase, Sale

from investment import serialisers


class InvestmentViewSet(viewsets.ModelViewSet):
    """View for managing Investment APIs."""

    serializer_class = serialisers.InvestmentSerialiser
    queryset = Investment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get Investments for authenticated user."""

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new Investment and make sure correct user is assigned."""

        serializer.save(user=self.request.user)


class PurchaseViewSet(viewsets.ModelViewSet):
    """View for managing Purchase APIs."""

    serializer_class = serialisers.PurchaseSerialiser
    queryset = Purchase.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get Investments for authenticated user."""

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new Investment and make sure correct user is assigned."""

        serializer.save(user=self.request.user)


class SaleViewSet(viewsets.ModelViewSet):
    """View for managing Sale APIs."""

    serializer_class = serialisers.SaleSerialiser
    queryset = Sale.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get Sales for authenticated user."""

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new Investment and make sure correct user is assigned."""

        serializer.save(user=self.request.user)


class HistoryViewSet(viewsets.ModelViewSet):
    """View for managing Sale APIs."""

    serializer_class = serialisers.HistorySerialiser
    queryset = History.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get History for authenticated user."""

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new History entry and make sure correct user is assigned."""

        serializer.save(user=self.request.user)
