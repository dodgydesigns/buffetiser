"""
Views for the Investment APIs.
"""

import json
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    def get_serializer_class(self):
        """Return the correct serializer for each action type."""
        if self.action == "list":
            return serialisers.InvestmentSerialiser
        elif self.action == "import_investments":
            return serialisers.InvestmentImportSerialiser

    def perform_create(self, serializer):
        """Create a new Investment and make sure correct user is assigned."""
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=False, url_path="import")
    def import_investments(self, request):
        """Create a number of Investment objects from user upload."""
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )

        if serializer.is_valid():
            payload = []
            for investment in serializer.data:
                investment.save()
                payload.append(json.dumps(investment))
            return Response(status=status.HTTP_200_OK)
        else:
            print("E E E E E E E E E E E E E E E E E E E E E E E E E")
            print(serializer.errors)
            print("E E E E E E E E E E E E E E E E E E E E E E E E E`")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
