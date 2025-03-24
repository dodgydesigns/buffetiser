from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import LogoutAndBlacklistRefreshTokenView  # Import custom logout view

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("docs/", include("docs.urls")),
    path("", include(router.urls)),
    path("", include("core.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAndBlacklistRefreshTokenView.as_view(), name='logout'),  # Use custom logout view
]
