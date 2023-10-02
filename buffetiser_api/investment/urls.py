"""
URL mappings for the Investment app.
"""


from investment import views
from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"investment", views.InvestmentViewSet)
router.register(r"purchase", views.PurchaseViewSet, basename="purchase")
router.register(r"sale", views.SaleViewSet, basename="sale")
app_name = "investment"

urlpatterns = [
    path('', include(router.urls)),
]
