from django.urls import path
from rest_framework import routers

from core import views
from core.views import AllInvestmentsDataView, InvestmentViewSet

router = routers.DefaultRouter()
router.register(r"investments", InvestmentViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("all/", AllInvestmentsDataView.as_view()),
    path("update_daily/", views.update_daily_changes),
    path("update_all/", views.update_all_investments),
]
