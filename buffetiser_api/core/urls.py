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
# from django.contrib import admin
# from django.urls import path

# from . import views

# urlpatterns = [
#     path("admin", admin.site.urls),
#     path("update_daily", views.update_daily_changes, name="update_daily"),
#     path("update_investments", views.update_all_investments, name="update_investments"),
#     path("", views.get_all_investments, name="get_all_investments"),
#     path("all", views.get_all_investments, name="get_all_investments"),
#     # path('<symbol>/', views.investmentDetails, name='Investment Details'),
#     # path('purchase', views.newPurchase, name='New Purchase'),
#     # path('add_purchase', views.addPurchase, name='Add Purchase'),
#     # path('config', views.config, name='Buffetiser Config'),
#     # path('live', views.updateLivePrices, name='Live Prices'),
#     # path('buffetiserHelp', views.buffetiserHelp, name='Buffetiser Help'),
# ]
