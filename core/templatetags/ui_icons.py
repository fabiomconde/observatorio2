"""Small inline SVG icon set for the public UI.

The project historically stores a few emoji values in the database.  This
helper keeps the data model intact while rendering those legacy values as
consistent, accessible SVG line icons in templates.
"""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ICONS = {
    "leaf": (
        '<path d="M20 4.5C13.5 4.5 7.5 7 5.2 12.1c-1.6 3.6.1 6.9 3.5 7.2 4.5.4 8.4-3.8 9.3-11.1"/>'
        '<path d="M5.5 19c2.2-3.2 5.5-5.9 10.1-8.2"/>'
    ),
    "droplet": '<path d="M12 3.5c-2.8 3.4-6 7.2-6 11a6 6 0 0 0 12 0c0-3.8-3.2-7.6-6-11Z"/>',
    "sun": (
        '<circle cx="12" cy="12" r="3.6"/>'
        '<path d="M12 2v2.1M12 19.9V22M4.93 4.93l1.48 1.48M17.59 17.59l1.48 1.48M2 12h2.1M19.9 12H22M4.93 19.07l1.48-1.48M17.59 6.41l1.48-1.48"/>'
    ),
    "compass": (
        '<circle cx="12" cy="12" r="9"/>'
        '<path d="m15.7 8.3-2.1 5.3-5.3 2.1 2.1-5.3 5.3-2.1Z"/>'
    ),
    "research": (
        '<circle cx="10.5" cy="10.5" r="5.5"/>'
        '<path d="m15 15 5 5M10.5 7.6v5.8M7.6 10.5h5.8"/>'
    ),
    "shield": (
        '<path d="M12 3 5.5 5.6v5.1c0 4.2 2.8 8 6.5 10.3 3.7-2.3 6.5-6.1 6.5-10.3V5.6L12 3Z"/>'
        '<path d="m9.3 12 1.8 1.8 3.8-4"/>'
    ),
    "map": (
        '<path d="m4 5 5-2 6 2 5-2v16l-5 2-6-2-5 2V5Z"/>'
        '<path d="M9 3v16M15 5v16"/>'
    ),
    "chart": (
        '<path d="M4 20V10h4v10H4ZM10 20V4h4v16h-4ZM16 20v-7h4v7h-4Z"/>'
    ),
    "people": (
        '<circle cx="9" cy="8" r="3"/>'
        '<path d="M3.8 20c.4-4 2.2-6 5.2-6s4.8 2 5.2 6"/>'
        '<path d="M15.5 5.8a2.7 2.7 0 0 1 0 5.2M16 14c2.7.2 4.1 2.1 4.4 5"/>'
    ),
    "layers": (
        '<path d="m12 3 9 5-9 5-9-5 9-5Z"/>'
        '<path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>'
    ),
    "globe": (
        '<circle cx="12" cy="12" r="9"/>'
        '<path d="M3.5 12h17M12 3c2.2 2.5 3.3 5.5 3.3 9S14.2 18.5 12 21M12 3C9.8 5.5 8.7 8.5 8.7 12S9.8 18.5 12 21"/>'
    ),
}

ALIASES = {
    "🌳": "leaf",
    "🌲": "leaf",
    "🌿": "leaf",
    "🌾": "leaf",
    "☀": "sun",
    "☀️": "sun",
    "💧": "droplet",
    "🔬": "research",
    "🧭": "compass",
    "🛡": "shield",
    "🛡️": "shield",
    "map": "map",
    "chart": "chart",
    "people": "people",
    "globe": "globe",
    "research": "research",
    "shield": "shield",
    "layers": "layers",
}


def _resolve_icon(value: object) -> str:
    token = str(value or "").strip()
    if token in ALIASES:
        return ALIASES[token]

    lowered = token.lower()
    hints = (
        ("droplet", "droplet"),
        ("water", "droplet"),
        ("tree", "leaf"),
        ("leaf", "leaf"),
        ("sun", "sun"),
        ("map", "map"),
        ("geo", "map"),
        ("people", "people"),
        ("person", "people"),
        ("shield", "shield"),
        ("search", "research"),
        ("diagram", "layers"),
        ("chart", "chart"),
        ("graph", "chart"),
        ("globe", "globe"),
    )
    for hint, icon_name in hints:
        if hint in lowered:
            return icon_name
    return "layers"


@register.simple_tag
def ui_icon(value="", size=24):
    """Render a decorative inline SVG, mapping legacy emoji/icon values."""
    try:
        safe_size = max(14, min(int(size), 72))
    except (TypeError, ValueError):
        safe_size = 24

    name = _resolve_icon(value)
    body = ICONS.get(name, ICONS["layers"])
    svg = (
        f'<svg class="ui-icon ui-icon-{name}" width="{safe_size}" height="{safe_size}" '
        'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
        f"{body}</svg>"
    )
    return mark_safe(svg)
