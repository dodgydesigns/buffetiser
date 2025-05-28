from django.urls import path
from rest_framework import routers

from core import views
from core.views import (AllConstantsView, AllInvestmentsDataView, BackupDBView,
                        ConfigView, CronTimeView, InvestmentViewSet,
                        RestoreDBView)

router = routers.DefaultRouter()
router.register(r"investments", InvestmentViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("all/", AllInvestmentsDataView.as_view()),
    path("constants/", AllConstantsView.as_view()),
    path("config/", ConfigView.as_view()),
    path("backup_db/", BackupDBView.as_view()),
    path("restore_db/<str:path>/", RestoreDBView.as_view()),
    path("cron_time/", CronTimeView.as_view()),
    path("update_daily/", views.update_daily_changes),
    path("update_all/", views.update_all_investments),
    path("portfolio/", views.PortfolioTotals.as_view()),
    path("new_investment/", views.NewInvestmentView.as_view()),
    path("purchase/", views.PurchaseView.as_view()),
    path("sale/", views.SaleView.as_view()),
    path("remove/", views.RemoveView.as_view()),
    path("reports/", views.ReportsView.as_view()),
    path("add_reinvestment/", views.DividendReinvestmentView.as_view()),
    path("add_dividend_payment/", views.DividendPaymentView.as_view()),
]
