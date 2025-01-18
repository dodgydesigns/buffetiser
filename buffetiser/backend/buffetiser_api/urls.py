from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path('docs/', include('docs.urls')),
    path("", include(router.urls)),
    path("", include("core.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]