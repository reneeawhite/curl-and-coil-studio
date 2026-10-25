"""Care Guide page: sourced before/during/after guidance for whichever style
the user picked in chat (or chose manually here), read from care_guidance.csv."""

from __future__ import annotations

from collections import defaultdict

import dash
from dash import Input, Output, callback, dcc, html

from components import icon
from data.load_data import load_care_guidance

dash.register_page(__name__, path="/care", name="Care Guide")

SERVICE_LABELS = {
    "box_knotless_braids": "Box / Knotless Braids",
    "twists_plaits_cornrows": "Twists, Plaits & Cornrows",
    "locs": "Locs",
}

# phase (care_guidance.csv) -> which before/during/after column it belongs in.
PHASE_TO_COLUMN = {
    "braid_preparation": "before",
    "braid_maintenance": "during",
    "natural_style_wash_styling": "during",
    "takedown": "after",
}
COLUMNS = [
    ("before", "comb", "Before your appointment"),
    ("during", "spray-bottle", "During your style"),
    ("after", "scissors", "Taking it down"),
]

# G07 is meta-commentary about a sourcing gap ("AAD gives no takedown procedure"),
# not actual guidance - G15-G17 already fill that exact gap with a real,
# dermatologist-sourced takedown procedure in the same column, so showing G07
# too would just confuse a user with an internal research note. Kept in the
# CSV for the data's own documentation trail; skipped here.
EXCLUDED_FROM_DISPLAY = {"G07"}

_UNINFORMATIVE_UNCERTAINTY = {"", "none noted", "none noted."}


def _guidance_card(row):
    children = [
        html.Div(row["step"], className="care-card-step"),
        html.P(row["plain_language_guidance"], className="care-card-guidance"),
        html.P(
            f"{row['source_title']} · checked {row['checked_at']}",
            className="care-card-source",
        ),
    ]
    uncertainty = (row.get("limits_or_uncertainty") or "").strip()
    if uncertainty.lower() not in _UNINFORMATIVE_UNCERTAINTY:
        children.append(html.Div(uncertainty, className="care-card-caveat"))
    return html.Div(children, className="care-card")


def _columns_for(service_path: str):
    rows = [
        r
        for r in load_care_guidance()
        if r["service_path"] == service_path and r["guidance_id"] not in EXCLUDED_FROM_DISPLAY
    ]
    by_column = defaultdict(list)
    for r in rows:
        column = PHASE_TO_COLUMN.get(r["phase"])
        if column:
            by_column[column].append(r)

    sections = []
    for column_key, icon_name, title in COLUMNS:
        column_rows = by_column.get(column_key, [])
        if column_rows:
            cards = [_guidance_card(r) for r in column_rows]
        else:
            cards = [
                html.P(
                    "No sourced guidance for this part yet - use your own judgment or ask a "
                    "dermatologist for anything style-specific here.",
                    className="care-card-empty",
                )
            ]
        sections.append(
            html.Div(
                className="care-column",
                children=[
                    html.Div(
                        [icon(icon_name), html.H3(title, className="care-column-title")],
                        className="care-column-header",
                    ),
                    html.Div(cards, className="care-column-list"),
                ],
            )
        )
    return sections


def _layout_for(service_path: str | None):
    if not service_path:
        return html.Div(
            className="empty-state",
            children=[
                html.Div(className="icon-row", children=[icon("spray-bottle"), icon("comb")]),
                html.P("Pick a style above (or tell the chat what you're after) to see before/during/after care."),
            ],
        )
    return html.Div(_columns_for(service_path), className="care-columns")


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
                            id="care-service-filter",
                            options=[{"label": v, "value": k} for k, v in SERVICE_LABELS.items()],
                            value=None,
                            placeholder="Choose a style to see its care guide",
                            clearable=False,
                            className="filter-dropdown",
                        ),
                    ],
                ),
                html.Div(id="care-guide-content", children=_layout_for(None)),
            ],
        )
    ],
)


@callback(
    Output("care-service-filter", "value"),
    Input("user-plan", "data"),
)
def _default_from_plan(plan):
    service_path = (plan or {}).get("service_path")
    return service_path or dash.no_update


@callback(
    Output("care-guide-content", "children"),
    Input("care-service-filter", "value"),
)
def _update_content(service_path):
    return _layout_for(service_path)
