"""Curl & Coil Studio - shared app shell (nav, decorative room, shared plan
state) for a multi-page Dash app. Each page's own layout/callbacks live in
pages/ (Dash Pages, auto-discovered from that folder).
"""

from __future__ import annotations

import dash
from dash import Dash, Input, Output, callback, dcc, html

from components import nav_bar, plan_summary_chip, scene_deco

app = Dash(__name__, use_pages=True, title="Curl & Coil Studio", suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div(
    children=[
        scene_deco(),
        dcc.Location(id="url"),
        dcc.Store(id="user-plan", storage_type="session", data={}),
        html.Div(
            className="salon-app",
            children=[
                html.Div(id="nav-bar-slot"),
                html.Div(id="plan-chip-slot"),
                dash.page_container,
            ],
        ),
    ]
)


@callback(Output("nav-bar-slot", "children"), Input("url", "pathname"))
def _render_nav(pathname):
    return nav_bar(pathname)


@callback(Output("plan-chip-slot", "children"), Input("user-plan", "data"))
def _render_plan_chip(plan):
    return plan_summary_chip(plan)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=8050)
