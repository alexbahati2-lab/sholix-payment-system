from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def home(request):
    return JsonResponse({
        "system": "Sholix Payment System",
        "short_name": "SPS",
        "status": "running",
        "message": "Welcome to the SPS backend API.",
        "health": "/api/health/",
        "admin": "/admin/",
    })


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("payments.urls")),
]