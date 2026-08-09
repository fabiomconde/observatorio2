"""
Template context processors that inject project-wide variables.
"""

from django.conf import settings


def site_meta(request):
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "MapBiomas Clone"),
        "SITE_TAGLINE": getattr(
            settings, "SITE_TAGLINE", "Monitoramento da cobertura e uso da terra"
        ),
        "SITE_DESCRIPTION": getattr(
            settings, "SITE_DESCRIPTION", "Iniciativa multi-institucional."
        ),
    }
