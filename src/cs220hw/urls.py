from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("rabble.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/", include("api.urls"))
]