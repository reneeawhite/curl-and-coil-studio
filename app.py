"""Restful Roots - shared app shell (nav, decorative room, shared plan
state) for a multi-page Dash app. Each page's own layout/callbacks live in
pages/ (Dash Pages, auto-discovered from that folder).
"""

from __future__ import annotations

import json
from urllib.parse import quote, unquote

import dash
from dash import Dash, Input, Output, callback, dcc, html
from flask import request

from components import nav_bar, plan_summary_chip, scene_deco

app = Dash(__name__, use_pages=True, title="Restful Roots", suppress_callback_exceptions=True)
server = app.server

PLAN_COOKIE = "restful_roots_plan"
PLAN_COOKIE_MAX_AGE = 60 * 60 * 24 * 180  # 180 days - an explicit, visible lifetime
# rather than a plan persisting silently forever.


def _serve_layout():
    """A function (not a static object) so it re-reads the cookie on every full page
    load - this is what lets the shared plan survive closing the tab or restarting the
    browser on this device, with no account/login needed. Plain server-side cookies
    were used instead of dcc.Store's own storage_type persistence or a clientside
    callback: both raced against this app's several different page-level callbacks that
    write the plan (home.py, products_catalog.py, providers_map.py) and unreliably lost
    updates in testing; a cookie travels with the request itself, so there's no client
    JS timing to get wrong.
    """
    raw_cookie = request.cookies.get(PLAN_COOKIE, "")
    try:
        restored_plan = json.loads(unquote(raw_cookie)) if raw_cookie else {}
    except ValueError:
        restored_plan = {}

    return html.Div(
        children=[
            scene_deco(),
            dcc.Location(id="url"),
            dcc.Store(id="user-plan", data=restored_plan),
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


app.layout = _serve_layout


@callback(Output("nav-bar-slot", "children"), Input("url", "pathname"))
def _render_nav(pathname):
    return nav_bar(pathname)


@callback(Output("plan-chip-slot", "children"), Input("user-plan", "data"))
def _render_plan_chip(plan):
    # The one place every plan update passes through (every page-level callback that
    # writes "user-plan" ends up here), so it's also the one place that needs to persist
    # the cookie - every writer doesn't need its own copy of this logic.
    dash.ctx.response.set_cookie(PLAN_COOKIE, quote(json.dumps(plan or {})), max_age=PLAN_COOKIE_MAX_AGE)
    return plan_summary_chip(plan)


@callback(
    Output("user-plan", "data", allow_duplicate=True),
    Input("clear-plan-btn", "n_clicks"),
    prevent_initial_call=True,
)
def _clear_plan(n_clicks):
    # Guard against n_clicks=0 the same way every other plan-writing callback does -
    # "Clear my plan" only exists in the DOM once the plan already has content, so this
    # button is *newly mounted* on whatever page load first shows a non-empty plan.
    # prevent_initial_call only suppresses the very first app-wide callback pass, not a
    # component's own first mount later in the session - without this guard, the button
    # appearing with its default n_clicks=0 fires this callback immediately and silently
    # wipes the plan that was just restored.
    if not n_clicks:
        return dash.no_update
    return {}


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=8050)
