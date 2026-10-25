"""Find a Stylist page: a real map of New Haven-area providers, filterable by
service path and budget tier, with a detail panel on marker click."""

from __future__ import annotations

from collections import defaultdict

import dash
from dash import ALL, Input, Output, State, callback, ctx, dcc, html

from components import icon
from data.load_data import load_providers, price_display, wash_blowdry_badges

dash.register_page(__name__, path="/providers", name="Find a Stylist")

SERVICE_LABELS = {
    "box_knotless_braids": "Box / Knotless Braids",
    "twists_plaits_cornrows": "Twists, Plaits & Cornrows",
    "locs": "Locs",
}
BUDGET_LABELS = {"low": "Low budget", "mid": "Mid budget", "high": "High budget"}


def _group_by_business(rows):
    groups = defaultdict(list)
    for row in rows:
        if row["lat"] is None or row["lon"] is None:
            continue
        groups[row["public_business_name"]].append(row)
    return groups


def _build_map_figure(service_filters: list, budget_filters: list):
    rows = load_providers()
    groups = _group_by_business(rows)

    lats, lons, names, ids = [], [], [], []
    for business_name, business_rows in groups.items():
        matching = [
            r
            for r in business_rows
            if (not service_filters or r["service_path"] in service_filters)
            and (not budget_filters or r["budget_tier"] in budget_filters)
        ]
        if not matching:
            continue
        rep = matching[0]
        lats.append(rep["lat"])
        lons.append(rep["lon"])
        names.append(business_name)
        ids.append(business_name)

    # Built as a plain dict, not go.Figure(go.Scattermap(...)): the installed Python
    # plotly (7.x) only emits the newer "scattermap" trace type, but the Plotly.js
    # bundled with this Dash version (4.1.1) is too old to render it - markers were
    # silently invisible. dcc.Graph accepts a plain dict figure directly, so this
    # bypasses go.Figure's strict trace-type validation and uses the older,
    # frontend-compatible "scattermapbox" trace / "mapbox" layout key instead.
    figure = {
        "data": [
            {
                "type": "scattermap",
                "lat": lats,
                "lon": lons,
                "mode": "markers",
                "marker": {"size": 20, "color": "#D85A26"},
                "text": names,
                "customdata": ids,
            }
        ],
        "layout": {
            "map": {
                # The bundled Plotly.js (4.1.1) only accepts a fixed set of named
                # style strings here and silently falls back to its default
                # ("carto-voyager") for anything else - this string is effectively
                # just a placeholder. assets/map_style_apply.js does the real work,
                # swapping in the recolored style (assets/map_style.json, CARTO's
                # free Positron basemap tinted to this app's cream/teal/terracotta
                # palette) via Plotly.relayout() after every render, since that API
                # does accept a full custom style object.
                "style": "carto-voyager",
                "center": {"lat": 41.313, "lon": -72.945},
                "zoom": 11.2,
            },
            "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
            "height": 420,
            "showlegend": False,
        },
    }
    return figure


def _detail_panel(business_name: str | None, plan: dict | None):
    if not business_name:
        return html.Div(
            className="empty-state",
            children=[
                html.Div(className="icon-row", children=[icon("map-pin")]),
                html.P("Click a pin on the map to see prices, ratings, and booking links for that stylist."),
            ],
        )
    rows = [r for r in load_providers() if r["public_business_name"] == business_name]
    if not rows:
        return html.P("That provider isn't in the current filter.")

    plan = plan or {}
    selected_ids = set(plan.get("selected_style_ids") or [])

    first = rows[0]
    # Rating is the same for every row at a given business (it's a per-business figure,
    # not per-service), so show it once in the header instead of repeating it on every card.
    rating_bits = []
    if first["rating_platform"] and first["rating_platform"] != "not confirmed":
        rating_bits.append(f"{first['rating_value']} on {first['rating_platform']}")
        if first["review_count"]:
            rating_bits.append(f"{first['review_count']} reviews")

    # Group by style so the budget badge can describe "this business, for this style"
    # once per group, rather than sitting on every line item - a single cheap add-on
    # (e.g. a $63 blow-dry) would otherwise carry the same badge as a $200 install from
    # the same style group, which reads as wrong even though the badge is describing
    # the business's overall pricing for that style, not that one line.
    by_style = defaultdict(list)
    for r in rows:
        by_style[r["service_path"]].append(r)

    style_sections = []
    for service_path in SERVICE_LABELS:
        style_rows = by_style.get(service_path)
        if not style_rows:
            continue
        cards = []
        for r in style_rows:
            is_selected = r["provider_id"] in selected_ids
            card_children = [
                html.Div(r["service"], className="provider-service-name"),
                html.Div(price_display(r), className="provider-service-price"),
            ]
            badges = wash_blowdry_badges(r)
            if badges:
                card_children.append(html.Div(" · ".join(badges), className="provider-service-wash"))
            card_children.append(
                html.A(
                    "Book / check availability",
                    href=r["booking_url"] if r["booking_url"] and r["booking_url"].startswith("http") else "#",
                    target="_blank",
                    className="provider-service-link",
                )
            )
            card_children.append(
                html.Button(
                    [icon("scissors"), "Remove this selection" if is_selected else "Select this style"],
                    id={"type": "select-style-btn", "index": r["provider_id"]},
                    n_clicks=0,
                    className="plan-action-btn plan-action-btn-small" + (" selected" if is_selected else ""),
                )
            )
            cards.append(
                html.Div(
                    card_children,
                    className="provider-service-card" + (" selected" if is_selected else ""),
                )
            )
        group_tier = style_rows[0]["budget_tier"]
        style_sections.append(
            html.Div(
                className="provider-style-group",
                children=[
                    html.Div(
                        className="provider-style-group-header",
                        children=[
                            html.Span(SERVICE_LABELS[service_path], className="provider-style-group-title"),
                            html.Div(
                                BUDGET_LABELS.get(group_tier, group_tier),
                                className=f"product-budget-badge product-budget-{group_tier}",
                            ),
                        ],
                    ),
                    html.Div(cards, className="provider-service-list"),
                ],
            )
        )

    return html.Div(
        children=[
            html.H3(business_name, className="detail-title"),
            html.P(
                " · ".join([first["neighborhood"], *rating_bits]) if rating_bits else first["neighborhood"],
                className="detail-sub",
            ),
            *style_sections,
        ]
    )


layout = html.Div(
    className="counter-wrap",
    children=[
        html.Div(
            className="chat-window",
            children=[
                html.Div(
                    className="filter-row",
                    children=[
                        dcc.Dropdown(
                            id="map-service-filter",
                            options=[{"label": v, "value": k} for k, v in SERVICE_LABELS.items()],
                            value=[],
                            multi=True,
                            placeholder="All styles",
                            className="filter-dropdown",
                        ),
                        dcc.Dropdown(
                            id="map-budget-filter",
                            options=[{"label": v, "value": k} for k, v in BUDGET_LABELS.items()],
                            value=[],
                            multi=True,
                            placeholder="Any budget",
                            className="filter-dropdown",
                        ),
                    ],
                ),
                dcc.Graph(id="provider-map", config={"displayModeBar": False}),
                html.Div(id="provider-detail-panel", className="detail-panel", children=_detail_panel(None, None)),
                dcc.Store(id="displayed-business-name", data=None),
            ],
        )
    ],
)


@callback(
    Output("provider-map", "figure"),
    Input("map-service-filter", "value"),
    Input("map-budget-filter", "value"),
)
def _update_map(service_filters, budget_filters):
    return _build_map_figure(service_filters, budget_filters)


@callback(
    Output("provider-detail-panel", "children"),
    Output("displayed-business-name", "data"),
    Input("provider-map", "clickData"),
    Input("user-plan", "data"),
    State("displayed-business-name", "data"),
)
def _update_detail(click_data, plan, displayed_business):
    if ctx.triggered_id == "provider-map" and click_data:
        business_name = click_data["points"][0]["customdata"]
    else:
        business_name = displayed_business
    return _detail_panel(business_name, plan), business_name


@callback(
    Output("user-plan", "data", allow_duplicate=True),
    Input({"type": "select-style-btn", "index": ALL}, "n_clicks"),
    State("user-plan", "data"),
    prevent_initial_call=True,
)
def _select_style(_n_clicks_list, plan):
    triggered_id = ctx.triggered_id
    triggered_value = ctx.triggered[0]["value"] if ctx.triggered else None
    if not triggered_id or not triggered_value:
        return dash.no_update
    provider_id = triggered_id["index"]
    plan = dict(plan or {})
    ids = list(plan.get("selected_style_ids") or [])
    if provider_id in ids:
        ids.remove(provider_id)
    else:
        ids.append(provider_id)
    plan["selected_style_ids"] = ids
    return plan
