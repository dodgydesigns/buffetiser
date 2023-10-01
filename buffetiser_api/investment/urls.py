"""
URL mappings for the Investment app.
"""


from investment import views
from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("investment", views.InvestmentViewSet)

app_name = "investment"

urlpatterns = [
    path('', include(router.urls))
]
