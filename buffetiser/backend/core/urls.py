from django.urls import path
from rest_framework import routers

from core.views import (AllConstantsView, AllInvestmentsDataView, BackupDBView,
                        ConfigView, CronTimeView, DividendPaymentView, DividendReinvestmentView, 
                        InvestmentViewSet, NewInvestmentView, PortfolioTotals, PurchaseView, 
                        RemoveView, ReportsView,
                        RestoreDBView, SaleView, update_all_investments, update_daily_changes)

router = routers.DefaultRouter()
router.register(r"investments", InvestmentViewSet)

urlpatterns = router.urls
urlpatterns += [
    path("all/", AllInvestmentsDataView.as_view()),
    path("portfolio/", PortfolioTotals.as_view()),
    path("constants/", AllConstantsView.as_view()),
    path("config/", ConfigView.as_view()),
    path("backup_db/", BackupDBView.as_view()),
    path("restore_db/<str:path>/", RestoreDBView.as_view()),
    path("cron_time/", CronTimeView.as_view()),
    path("update_daily/", update_daily_changes),
    path("update_all/", update_all_investments),
    path("new_investment/", NewInvestmentView.as_view()),
    path("purchase/", PurchaseView.as_view()),
    path("sale/", SaleView.as_view()),
    path("remove/", RemoveView.as_view()),
    path("reports/", ReportsView.as_view()),
    path("add_reinvestment/", DividendReinvestmentView.as_view()),
    path("add_dividend_payment/", DividendPaymentView.as_view()),
]
