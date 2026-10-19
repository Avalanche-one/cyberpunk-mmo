from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("user.urls")),
    path("", include("cyberpunk_mmo.urls")),
]
