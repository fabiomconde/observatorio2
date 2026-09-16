"""Inline SVG helpers for the public UI.

The database stores legacy emoji/icon values for some content.  We keep that
model intact, but render semantic SVGs in the interface.

SVG path data in this module is adapted from Tabler Icons:
https://github.com/tabler/tabler-icons
MIT License — Copyright (c) 2020-2026 Paweł Kuna.

The mapping intentionally prefers the *meaning* of each pillar title over the
raw emoji, so a scale stays a scale, a map stays a map, etc.
"""

from __future__ import annotations

import unicodedata

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Tabler Icons outline paths. All icons use the canonical 24x24 viewBox and
# currentColor so the institutional palette can be controlled entirely in CSS.
ICONS = {
    "scale": (
        '<path d="M7 20l10 0" />'
        '<path d="M6 6l6 -1l6 1" />'
        '<path d="M12 3l0 17" />'
        '<path d="M9 12l-3 -6l-3 6a3 3 0 0 0 6 0" />'
        '<path d="M21 12l-3 -6l-3 6a3 3 0 0 0 6 0" />'
    ),
    "sun-wind": (
        '<path d="M14.468 10a4 4 0 1 0 -5.466 5.46" />'
        '<path d="M2 12h1" />'
        '<path d="M11 3v1" />'
        '<path d="M11 20v1" />'
        '<path d="M4.6 5.6l.7 .7" />'
        '<path d="M17.4 5.6l-.7 .7" />'
        '<path d="M5.3 17.7l-.7 .7" />'
        '<path d="M15 13h5a2 2 0 1 0 0 -4" />'
        '<path d="M12 16h5.714l.253 0a2 2 0 0 1 2.033 2a2 2 0 0 1 -2 2h-.286" />'
    ),
    "map-2": (
        '<path d="M12 18.5l-3 -1.5l-6 3v-13l6 -3l6 3l6 -3v7.5" />'
        '<path d="M9 4v13" />'
        '<path d="M15 7v5.5" />'
        '<path d="M21.121 20.121a3 3 0 1 0 -4.242 0c.418 .419 1.125 1.045 2.121 1.879c1.051 -.89 1.759 -1.516 2.121 -1.879" />'
        '<path d="M19 18v.01" />'
    ),
    "book-2": (
        '<path d="M19 4v16h-12a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2h12" />'
        '<path d="M19 16h-12a2 2 0 0 0 -2 2" />'
        '<path d="M9 8h6" />'
    ),
    "network": (
        '<path d="M6 9a6 6 0 1 0 12 0a6 6 0 0 0 -12 0" />'
        '<path d="M12 3c1.333 .333 2 2.333 2 6s-.667 5.667 -2 6" />'
        '<path d="M12 3c-1.333 .333 -2 2.333 -2 6s.667 5.667 2 6" />'
        '<path d="M6 9h12" />'
        '<path d="M3 20h7" />'
        '<path d="M14 20h7" />'
        '<path d="M10 20a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />'
        '<path d="M12 15v3" />'
    ),
    "eye-check": (
        '<path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />'
        '<path d="M11.102 17.957c-3.204 -.307 -5.904 -2.294 -8.102 -5.957c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6a19.5 19.5 0 0 1 -.663 1.032" />'
        '<path d="M15 19l2 2l4 -4" />'
    ),
    "speakerphone": (
        '<path d="M18 8a3 3 0 0 1 0 6" />'
        '<path d="M10 8v11a1 1 0 0 1 -1 1h-1a1 1 0 0 1 -1 -1v-5" />'
        '<path d="M12 8l4.524 -3.77a.9 .9 0 0 1 1.476 .692v12.156a.9 .9 0 0 1 -1.476 .692l-4.524 -3.77h-8a1 1 0 0 1 -1 -1v-4a1 1 0 0 1 1 -1h8" />'
    ),
    "chart-bar": (
        '<path d="M3 13a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -6" />'
        '<path d="M15 9a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -10" />'
        '<path d="M9 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v14a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1l0 -14" />'
        '<path d="M4 20h14" />'
    ),
    "users-group": (
        '<path d="M10 13a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />'
        '<path d="M8 21v-1a2 2 0 0 1 2 -2h4a2 2 0 0 1 2 2v1" />'
        '<path d="M15 5a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />'
        '<path d="M17 10h2a2 2 0 0 1 2 2v1" />'
        '<path d="M5 5a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />'
        '<path d="M3 13v-1a2 2 0 0 1 2 -2h2" />'
    ),
}

PILLAR_RULES = (
    (("conflito", "direitos humanos"), "scale"),
    (("justica climatica", "equidade"), "sun-wind"),
    (("territorialidade", "integracao"), "map-2"),
    (("conhecimento", "evidencias"), "book-2"),
    (("interdisciplinaridade", "colaboracao"), "network"),
    (("transparencia", "etica", "responsabilidade"), "eye-check"),
    (("incidencia", "transformacao social"), "speakerphone"),
)

LEGACY_ALIASES = {
    "⚖": "scale",
    "⚖️": "scale",
    "🌍": "sun-wind",
    "🌎": "sun-wind",
    "🌏": "sun-wind",
    "🗺": "map-2",
    "🗺️": "map-2",
    "📖": "book-2",
    "📚": "book-2",
    "🤝": "network",
    "👁": "eye-check",
    "👁️": "eye-check",
    "✊": "speakerphone",
    "✊🏻": "speakerphone",
    "✊🏼": "speakerphone",
    "✊🏽": "speakerphone",
    "✊🏾": "speakerphone",
    "✊🏿": "speakerphone",
    "chart": "chart-bar",
    "map": "map-2",
    "people": "users-group",
}


def _normalize(value: object) -> str:
    text = str(value or "").strip().lower()
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _render(name: str, size: object = 24, css_class: str = ""):
    try:
        safe_size = max(14, min(int(size), 72))
    except (TypeError, ValueError):
        safe_size = 24

    icon_name = name if name in ICONS else "chart-bar"
    extra_class = f" {css_class.strip()}" if css_class and css_class.strip() else ""
    body = ICONS[icon_name]
    svg = (
        f'<svg class="ui-icon ui-icon-{icon_name}{extra_class}" '
        f'width="{safe_size}" height="{safe_size}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true" focusable="false">'
        f"{body}</svg>"
    )
    return mark_safe(svg)


@register.simple_tag
def ui_icon(value="", size=24, css_class=""):
    """Render one named semantic SVG (or map a legacy emoji)."""
    token = str(value or "").strip()
    name = LEGACY_ALIASES.get(token, token)
    return _render(name, size, css_class)


@register.simple_tag
def pillar_icon(title="", legacy_value="", size=32):
    """Choose an SVG from the pillar meaning, falling back to the old emoji."""
    normalized = _normalize(title)
    for keywords, icon_name in PILLAR_RULES:
        if all(keyword in normalized for keyword in keywords):
            return _render(icon_name, size, "pillar-svg")

    legacy = LEGACY_ALIASES.get(str(legacy_value or "").strip())
    return _render(legacy or "book-2", size, "pillar-svg")
