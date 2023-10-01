"""
Views for the Investment APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Investment

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
