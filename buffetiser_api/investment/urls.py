"""
URL mappings for the Investment app.
"""


from investment import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"investment", views.InvestmentViewSet)
router.register(r"purchase", views.PurchaseViewSet, basename="purchase")
router.register(r"sale", views.SaleViewSet, basename="sale")
router.register(r"history", views.HistoryViewSet, basename="history")

app_name = "investment"

urlpatterns = [
    path("", include(router.urls)),
]


# <URLPattern '^investment/$' [name='investment-list']>,
# <URLPattern '^investment\.(?P<format>[a-z0-9]+)/?$' [name='investment-list']>,
# <URLPattern '^investment/(?P<pk>[^/.]+)/$' [name='investment-detail']>,
# <URLPattern '^investment/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='investment-detail']>,
# <URLPattern '^purchase/$' [name='purchase-list']>,
# <URLPattern '^purchase\.(?P<format>[a-z0-9]+)/?$' [name='purchase-list']>,
# <URLPattern '^purchase/(?P<pk>[^/.]+)/$' [name='purchase-detail']>,
# <URLPattern '^purchase/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='purchase-detail']>,
# <URLPattern '^sale/$' [name='sale-list']>,
# <URLPattern '^sale\.(?P<format>[a-z0-9]+)/?$' [name='sale-list']>,
# <URLPattern '^sale/(?P<pk>[^/.]+)/$' [name='sale-detail']>,
# <URLPattern '^sale/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='sale-detail']>,
# <URLPattern '^$' [name='api-root']>,
# <URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>]
