"""Shared UI pieces used by the app shell (app.py) and every page in pages/:
icons, the decorative shelved-room background, the nav bar, and the small
"your plan so far" summary chip."""

from __future__ import annotations

import dash
from dash import dcc, html


def icon(name: str, class_name: str = "icon") -> html.Img:
    return html.Img(src=f"/assets/icons/{name}.svg", className=class_name, alt="")


NAV_ITEMS = [
    ("mirror", "Chat", "/"),
    ("map-pin", "Find a Stylist", "/providers"),
    ("spray-bottle", "Care Guide", "/care"),
    ("shopping-bag", "Shop Products", "/products"),
]


def nav_bar(pathname: str | None):
    pathname = pathname or "/"
    links = []
    for icon_name, label, href in NAV_ITEMS:
        active = pathname == href
        links.append(
            dcc.Link(
                [icon(icon_name), html.Span(label)],
                href=href,
                className=f"nav-link{' active' if active else ''}",
            )
        )
    return html.Div(links, className="salon-nav")


def plan_summary_chip(plan: dict | None):
    """A compact 'your plan so far' strip, shown once the chat has recorded anything."""
    plan = plan or {}
    parts = []
    labels = {
        "service_path": {
            "box_knotless_braids": "Box/Knotless Braids",
            "twists_plaits_cornrows": "Twists, Plaits & Cornrows",
            "locs": "Locs",
        },
        "neighborhood": None,
        "budget_tier": {"low": "Low budget", "mid": "Mid budget", "high": "High budget"},
        "prep_time": None,
    }
    for field, mapping in labels.items():
        value = plan.get(field)
        if not value:
            continue
        text = mapping.get(value, value) if mapping else value
        parts.append(html.Span(text, className="plan-chip-item"))
    if plan.get("selected_style_ids"):
        n = len(plan["selected_style_ids"])
        parts.append(html.Span(f"{n} style{'s' if n != 1 else ''} selected", className="plan-chip-item"))
    if plan.get("selected_product_ids"):
        parts.append(html.Span(f"{len(plan['selected_product_ids'])} product(s) added", className="plan-chip-item"))
    if not parts:
        return html.Div()
    return html.Div(
        [html.Span("Your plan so far:", className="plan-chip-label"), *parts],
        className="plan-chip-row",
    )


def _shelf(side: str, top_vh: float, width_px: int, items: list[tuple[str, int, int]]):
    """One wood shelf bar anchored to the wall band (0-66vh), with icons sitting on top.

    items: list of (icon_name, size_px, offset_px_from_shelf_edge)
    """
    edge_prop = "left" if side == "left" else "right"
    children = [
        html.Div(
            className="shelf-bar",
            style={edge_prop: "4px", "top": f"{top_vh}vh", "width": f"{width_px}px"},
        )
    ]
    for icon_name, size, offset in items:
        children.append(
            html.Img(
                src=f"/assets/icons/{icon_name}.svg",
                style={
                    edge_prop: f"{4 + offset}px",
                    "top": f"calc({top_vh}vh - {size - 6}px)",
                    "width": f"{size}px",
                    "height": f"{size}px",
                },
            )
        )
    return children


def scene_deco():
    """Fixed background layer: wood shelves (holding plants, framed pictures,
    and hair tools) mounted on the cream wall band, plus floor plants - a real
    shelved salon room, not icons scattered on flat color."""
    children = []
    # Each shelf's width and item offsets are computed so the three items sit
    # centered with even gaps between them and even margins at both shelf
    # ends (10px margin, 8px gap) - previously the offsets were eyeballed and
    # either overflowed past the shelf's right edge or overlapped each other.
    children += _shelf("left", 10, 224, [("plant", 90, 10), ("hairbrush", 48, 108), ("frame", 50, 164)])
    children += _shelf("left", 36, 214, [("comb", 44, 10), ("plant-broad", 80, 62), ("shampoo-bottle", 54, 150)])
    children += _shelf("right", 14, 230, [("plant-broad", 94, 10), ("blow-dryer", 50, 112), ("frame", 50, 170)])
    children += _shelf("right", 40, 212, [("shampoo-bottle", 54, 10), ("plant", 78, 72), ("comb", 44, 158)])
    # Flush to the viewport bottom (0, not a few px up) so the pot sits ON the
    # floor band instead of floating with a gap above the wall/floor seam.
    children.append(
        html.Img(
            src="/assets/icons/plant-broad.svg",
            style={"left": "6px", "bottom": "0", "width": "110px", "height": "128px"},
        )
    )
    children.append(
        html.Img(
            src="/assets/icons/plant.svg",
            style={"right": "6px", "bottom": "0", "width": "100px", "height": "117px"},
        )
    )
    return html.Div(children, className="scene-deco")
