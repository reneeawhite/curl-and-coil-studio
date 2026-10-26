"""Shop Products page: every sourced product grouped by brand, filterable by
service path, phase, budget tier, product type, and brand. Clicking a product
keeps it highlighted and opens its detail inline, right after its own card,
with an Add/Remove action wired into the shared plan store."""

from __future__ import annotations

from collections import defaultdict

import dash
from dash import ALL, Input, Output, State, callback, ctx, dcc, html

from components import icon
from data.load_data import is_stale, load_products, product_service_paths

dash.register_page(__name__, path="/products", name="Shop Products")

SERVICE_LABELS = {
    "box_knotless_braids": "Box / Knotless Braids",
    "twists_plaits_cornrows": "Twists, Plaits & Cornrows",
    "locs": "Locs",
}
PHASE_LABELS = {
    "braid_preparation": "Before (prep)",
    "braid_maintenance": "During (maintenance)",
    "natural_style_wash_styling": "Wash day & styling",
}
BUDGET_LABELS = {"low": "Low budget", "mid": "Mid budget", "high": "High budget"}
PRODUCT_TYPE_LABELS = {
    "shampoo": "Shampoo",
    "conditioner": "Conditioner",
    "oil": "Oil",
    "gel": "Gel",
    "spray": "Spray",
    "moisturizer_cream": "Moisturizer / Cream",
}
FALLBACK_ICON = "shampoo-bottle"


def _price_display(p):
    return f"${p['price_usd']:g}" if p["price_usd"] is not None else "Price not listed"


def _filtered_products(brands, services, phases, budgets, product_types):
    """Each filter arg is a list of selected values from a multi-select dropdown -
    an empty list means that filter is inactive (matches everything). Within one
    filter, a product matches if it hits ANY selected value (e.g. brand A OR brand
    B); across different filters, all active filters must match (AND)."""
    rows = load_products()
    return [
        r
        for r in rows
        if (not brands or r["brand"] in brands)
        and (not services or any(s in product_service_paths(r) for s in services))
        and (not phases or r["phase"] in phases)
        and (not budgets or r["budget_tier"] in budgets)
        and (not product_types or r["product_type"] in product_types)
    ]


def _product_card(p, selected_id):
    is_selected = p["product_id"] == selected_id
    media = (
        html.Img(src=p["image_url"], className="product-card-img")
        if p.get("image_url")
        else html.Div(icon(FALLBACK_ICON, class_name="product-card-icon-img"), className="product-card-img product-card-icon")
    )
    return html.Div(
        id={"type": "product-card", "index": p["product_id"]},
        n_clicks=0,
        className="product-card" + (" selected" if is_selected else ""),
        children=[
            media,
            html.Div(p["product_name"], className="product-card-name"),
            html.Div(_price_display(p), className="product-card-price"),
            html.Div(
                BUDGET_LABELS.get(p["budget_tier"], p["budget_tier"]),
                className=f"product-budget-badge product-budget-{p['budget_tier']}",
            ),
        ],
    )


def _checked_line(checked_at):
    """A plain checked-date line, or a visible re-check flag once that date is
    more than data.load_data.STALE_AFTER_DAYS old - this app's prices and
    claims are a dated snapshot, not a live feed (see scripts/
    check_data_freshness.py), so an old date should look different from a
    fresh one instead of reading the same either way."""
    if not checked_at:
        return None
    if is_stale(checked_at):
        return html.P(
            f"⚠ Checked {checked_at} — this is past this app's {90}-day re-check window; verify on the official page before trusting it.",
            className="product-detail-stale",
        )
    return html.P(f"Checked {checked_at}", className="product-detail-checked")


def _detail_inline(p, plan):
    in_plan = p["product_id"] in (plan or {}).get("selected_product_ids", [])
    link = p["official_product_url"] if p["official_product_url"].startswith("http") else p["other_source_url"]
    checked_line = _checked_line(p.get("checked_at"))
    return html.Div(
        className="product-detail-inline",
        children=[
            html.H3(p["product_name"], className="detail-title"),
            html.P(f"{p['brand']} · {p['size']} · {_price_display(p)}", className="detail-sub"),
            html.P(p["target_need"], className="product-detail-need"),
            html.P(p["usage_notes"], className="product-detail-usage"),
            html.P(p["source_supported_claim"], className="product-detail-source"),
            *([checked_line] if checked_line else []),
            html.A(
                "View product page",
                href=link if link and link.startswith("http") else "#",
                target="_blank",
                className="provider-service-link",
            ),
            html.Button(
                [icon("shopping-bag"), "Remove from my plan" if in_plan else "Add to my plan"],
                id="product-plan-toggle-btn",
                n_clicks=0,
                className="plan-action-btn" + (" selected" if in_plan else ""),
            ),
        ],
    )


def _brand_sections(products, selected_id, plan):
    if not products:
        return html.Div(
            className="empty-state",
            children=[html.P("No products match these filters - try widening the budget or style.")],
        )
    by_brand = defaultdict(list)
    for p in products:
        by_brand[p["brand"]].append(p)

    sections = []
    for brand in sorted(by_brand):
        cards = []
        for p in by_brand[brand]:
            cards.append(_product_card(p, selected_id))
            if p["product_id"] == selected_id:
                cards.append(_detail_inline(p, plan))
        sections.append(
            html.Div(
                className="product-brand-section",
                children=[
                    html.H3(brand, className="product-brand-title"),
                    html.Div(cards, className="product-grid"),
                ],
            )
        )
    return sections


def _filter_dropdowns():
    products = load_products()
    brands = sorted({p["brand"] for p in products})
    phases = [k for k in PHASE_LABELS if any(p["phase"] == k for p in products)]
    product_types = [k for k in PRODUCT_TYPE_LABELS if any(p["product_type"] == k for p in products)]
    return html.Div(
        className="filter-row",
        children=[
            dcc.Dropdown(
                id="product-brand-filter",
                options=[{"label": b, "value": b} for b in brands],
                value=[],
                multi=True,
                placeholder="All brands",
                className="filter-dropdown",
            ),
            dcc.Dropdown(
                id="product-service-filter",
                options=[{"label": v, "value": k} for k, v in SERVICE_LABELS.items()],
                value=[],
                multi=True,
                placeholder="All styles",
                className="filter-dropdown",
            ),
            dcc.Dropdown(
                id="product-phase-filter",
                options=[{"label": PHASE_LABELS[k], "value": k} for k in phases],
                value=[],
                multi=True,
                placeholder="Before, during, or wash day",
                className="filter-dropdown",
            ),
            dcc.Dropdown(
                id="product-budget-filter",
                options=[{"label": v, "value": k} for k, v in BUDGET_LABELS.items()],
                value=[],
                multi=True,
                placeholder="Any budget",
                className="filter-dropdown",
            ),
            dcc.Dropdown(
                id="product-type-filter",
                options=[{"label": PRODUCT_TYPE_LABELS[k], "value": k} for k in product_types],
                value=[],
                multi=True,
                placeholder="All product types",
                className="filter-dropdown",
            ),
        ],
    )


layout = html.Div(
    className="counter-wrap",
    children=[
        html.Div(
            className="chat-window",
            children=[
                _filter_dropdowns(),
                html.P(
                    "Click a product to see what it's for, how to use it, and where that information comes from.",
                    className="product-hint",
                ),
                html.Div(id="product-grid-container", children=_brand_sections(load_products(), None, None)),
                dcc.Store(id="selected-product-id", data=None),
            ],
        )
    ],
)


@callback(
    Output("product-grid-container", "children"),
    Input("product-brand-filter", "value"),
    Input("product-service-filter", "value"),
    Input("product-phase-filter", "value"),
    Input("product-budget-filter", "value"),
    Input("product-type-filter", "value"),
    Input("selected-product-id", "data"),
    Input("user-plan", "data"),
)
def _update_grid(brands, services, phases, budgets, product_types, selected_id, plan):
    return _brand_sections(_filtered_products(brands, services, phases, budgets, product_types), selected_id, plan)


@callback(
    Output("selected-product-id", "data"),
    Input({"type": "product-card", "index": ALL}, "n_clicks"),
    State("selected-product-id", "data"),
    prevent_initial_call=True,
)
def _select_product(_n_clicks_list, current_selected):
    triggered_id = ctx.triggered_id
    triggered_value = ctx.triggered[0]["value"] if ctx.triggered else None
    if not triggered_id or not triggered_value:
        return dash.no_update
    clicked_id = triggered_id["index"]
    # Click the already-selected card again to close its inline detail.
    return None if clicked_id == current_selected else clicked_id


@callback(
    Output("user-plan", "data", allow_duplicate=True),
    Input("product-plan-toggle-btn", "n_clicks"),
    State("selected-product-id", "data"),
    State("user-plan", "data"),
    prevent_initial_call=True,
)
def _toggle_product_in_plan(n_clicks, product_id, plan):
    if not n_clicks or not product_id:
        return dash.no_update
    plan = dict(plan or {})
    ids = list(plan.get("selected_product_ids") or [])
    if product_id in ids:
        ids.remove(product_id)
    else:
        ids.append(product_id)
    plan["selected_product_ids"] = ids
    return plan
