"""
URL configuration for the Observatório Socioambiental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

# Convenience: /favicon.ico -> static file
urlpatterns += [
    path(
        "favicon.ico",
        RedirectView.as_view(url=settings.STATIC_URL + "core/img/favicon.svg", permanent=True),
    ),
]

# Serve media & static in DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"
