"""Home page: the chat that builds the user's plan. Registered at "/"."""

from __future__ import annotations

from collections import defaultdict

import dash
from dash import ALL, Input, Output, State, callback, ctx, dcc, html

from agent.planner import run_turn
from components import icon
from data.load_data import load_products, load_providers

dash.register_page(__name__, path="/", name="Chat")

WELCOME = (
    "Hi! I'm your textured-hair planning buddy. Tell me what service you're after "
    "(knotless braids, twists, locs...) and I'll pull up real New Haven stylists, a prep & "
    "care plan, and a few products that fit your budget."
)

SERVICE_LABELS = {
    "box_knotless_braids": "Box / Knotless Braids",
    "twists_plaits_cornrows": "Twists, Plaits & Cornrows",
    "locs": "Locs",
}
FALLBACK_PRODUCT_ICON = "shampoo-bottle"

# A safety ceiling on real model spend per browser session - nothing else in this
# app currently stops a bug or a script sending rapid-fire messages from running
# up real cost (see HARNESS.md / the final report's Safety section). $0.25 is
# roughly 35-40x a single typical planning conversation (~$0.0066), generous for
# real use but not unbounded.
SESSION_COST_CAP_USD = 0.25
SESSION_CAP_MESSAGE = (
    f"This browser session has reached its ${SESSION_COST_CAP_USD:.2f} safety budget for model "
    "calls, so I can't send this one to the planner. Refresh the page to start a fresh session "
    "(your plan stays saved), or come back later - this cap exists to stop a bug or a runaway "
    "script from burning through real cost unnoticed."
)


def _session_cap_reached(usage_total: dict) -> bool:
    return usage_total.get("cost_usd", 0.0) >= SESSION_COST_CAP_USD


def _plan_summary_panel(plan: dict | None):
    """The full "your plan so far" view, shown on the home page per the project
    owner's request - the chip in the nav stays as a lightweight indicator
    everywhere else, this is the one place to review and remove choices."""
    plan = plan or {}
    service_path = plan.get("service_path")
    style_ids = plan.get("selected_style_ids") or []
    product_ids = plan.get("selected_product_ids") or []

    if not (service_path or style_ids or product_ids):
        return html.Div()

    items = []

    if service_path:
        items.append(
            html.Div(
                [icon("scissors"), html.Span(SERVICE_LABELS.get(service_path, service_path))],
                className="plan-panel-item",
            )
        )

    if style_ids:
        providers_by_id = {r["provider_id"]: r for r in load_providers()}
        selected_styles = [providers_by_id[sid] for sid in style_ids if sid in providers_by_id]
        by_business = defaultdict(list)
        for r in selected_styles:
            by_business[r["public_business_name"]].append(r)
        for business in sorted(by_business):
            business_rows = by_business[business]
            business_label = business if len(business_rows) == 1 else f"{business} ({len(business_rows)})"
            items.append(html.Div(business_label, className="plan-panel-brand-label"))
            for r in business_rows:
                items.append(
                    html.Div(
                        [
                            icon("map-pin"),
                            html.Span(r["service"]),
                            html.Button(
                                "Remove",
                                id={"type": "remove-style-btn", "index": r["provider_id"]},
                                n_clicks=0,
                                className="plan-remove-btn",
                            ),
                        ],
                        className="plan-panel-item",
                    )
                )

    if product_ids:
        products_by_id = {p["product_id"]: p for p in load_products()}
        selected_products = [products_by_id[pid] for pid in product_ids if pid in products_by_id]
        by_brand = defaultdict(list)
        for p in selected_products:
            by_brand[p["brand"]].append(p)
        for brand in sorted(by_brand):
            brand_products = by_brand[brand]
            brand_label = brand if len(brand_products) == 1 else f"{brand} ({len(brand_products)})"
            items.append(html.Div(brand_label, className="plan-panel-brand-label"))
            for p in brand_products:
                media = (
                    html.Img(src=p["image_url"], className="plan-panel-product-img")
                    if p.get("image_url")
                    else icon(FALLBACK_PRODUCT_ICON, class_name="plan-panel-product-icon")
                )
                items.append(
                    html.Div(
                        [
                            media,
                            html.Span(p["product_name"]),
                            html.Button(
                                "Remove",
                                id={"type": "remove-product-btn", "index": p["product_id"]},
                                n_clicks=0,
                                className="plan-remove-btn",
                            ),
                        ],
                        className="plan-panel-item",
                    )
                )

    return html.Div(
        className="plan-summary-panel",
        children=[
            html.H3("Your plan so far", className="plan-panel-title"),
            html.Div(items, className="plan-panel-list"),
        ],
    )


def _message_row(role: str, text: str):
    avatar_src = "avatar-stylist" if role == "agent" else "avatar-user"
    bubble = (
        dcc.Markdown(text, link_target="_blank", className=f"bubble {role}")
        if role == "agent"
        else html.Div(text, className=f"bubble {role}")
    )
    return html.Div(
        className=f"msg-row {role}",
        children=[
            html.Div(icon(avatar_src, "icon"), className="avatar"),
            bubble,
        ],
    )


def _render_chat(messages: list[dict]):
    if not messages:
        return html.Div(
            className="empty-state",
            children=[
                html.Div(
                    className="icon-row",
                    children=[icon("salon-chair"), icon("mirror"), icon("plant")],
                ),
                html.P(WELCOME),
            ],
        )
    return [_message_row(m["role"], m["text"]) for m in messages]


layout = html.Div(
    children=[
        html.Div(
            className="salon-header",
            children=[
                html.H1("Restful Roots", className="salon-title"),
                html.P(
                    "New Haven braid & protective-style planner - sourced stylists, care plans, and products",
                    className="salon-subtitle",
                ),
                html.Div(
                    className="salon-chip-row",
                    children=[
                        html.Span([icon("scissors"), "Knotless & Box Braids"], className="salon-chip c-teal"),
                        html.Span([icon("plant"), "Twists, Plaits & Cornrows"], className="salon-chip c-terracotta"),
                        html.Span([icon("plant-broad"), "Locs"], className="salon-chip c-leaf"),
                        html.Span([icon("mirror"), "Sourced & Dated"], className="salon-chip c-mustard"),
                    ],
                ),
            ],
        ),
        html.Div(id="plan-summary-slot", children=_plan_summary_panel(None)),
        html.Div(
            className="counter-wrap",
            children=[
                dcc.Loading(
                    type="circle",
                    color="#0D9488",
                    children=html.Div(id="chat-window", className="chat-window", children=_render_chat([])),
                ),
                html.Div(
                    className="salon-counter",
                    children=[
                        html.Div(
                            className="counter-tools",
                            children=[icon("comb"), icon("spray-bottle"), icon("hairbrush"), icon("shampoo-bottle")],
                        ),
                        html.Div(
                            className="input-row",
                            children=[
                                dcc.Input(
                                    id="user-input",
                                    type="text",
                                    placeholder="e.g. I want knotless braids, budget is low...",
                                    autoComplete="off",
                                    n_submit=0,
                                ),
                                html.Button(
                                    [icon("scissors"), html.Span("Send", className="send-btn-label")],
                                    id="send-btn",
                                    n_clicks=0,
                                ),
                            ],
                        ),
                        html.Div(id="usage-footer", className="usage-footer", children="No messages yet."),
                    ],
                ),
            ],
        ),
        dcc.Store(id="agent-history", data=None),
        dcc.Store(id="display-messages", data=[]),
        dcc.Store(id="usage-total", data={"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}),
    ]
)


@callback(
    Output("chat-window", "children"),
    Output("agent-history", "data"),
    Output("display-messages", "data"),
    Output("usage-total", "data"),
    Output("user-input", "value"),
    Output("usage-footer", "children"),
    Output("user-plan", "data", allow_duplicate=True),
    Input("send-btn", "n_clicks"),
    Input("user-input", "n_submit"),
    State("user-input", "value"),
    State("agent-history", "data"),
    State("display-messages", "data"),
    State("usage-total", "data"),
    State("user-plan", "data"),
    prevent_initial_call=True,
)
def send_message(_n_clicks, _n_submit, user_text, agent_history, display_messages, usage_total, plan):
    user_text = (user_text or "").strip()
    display_messages = display_messages or []
    usage_total = usage_total or {"input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}

    if not user_text:
        return (
            _render_chat(display_messages),
            agent_history,
            display_messages,
            usage_total,
            "",
            _usage_text(usage_total),
            plan,
        )

    display_messages = display_messages + [{"role": "user", "text": user_text}]

    if _session_cap_reached(usage_total):
        reply = SESSION_CAP_MESSAGE
    else:
        try:
            result = run_turn(user_text, agent_history, plan)
            reply = result["reply"]
            agent_history = result["history"]
            plan = result["plan"]
            usage_total = {
                "input_tokens": usage_total["input_tokens"] + result["input_tokens"],
                "output_tokens": usage_total["output_tokens"] + result["output_tokens"],
                "cost_usd": round(usage_total["cost_usd"] + result["cost_usd"], 6),
            }
        except Exception as exc:  # keep the chat alive even if the model/tool call fails
            reply = (
                "Sorry, something went wrong reaching the planner (" + str(exc) + "). "
                "Check that PORTKEY_API_KEY is set and try again."
            )

    display_messages = display_messages + [{"role": "agent", "text": reply}]

    return (
        _render_chat(display_messages),
        agent_history,
        display_messages,
        usage_total,
        "",
        _usage_text(usage_total),
        plan,
    )


@callback(
    Output("plan-summary-slot", "children"),
    Input("user-plan", "data"),
)
def _render_plan_summary(plan):
    return _plan_summary_panel(plan)


@callback(
    Output("user-plan", "data", allow_duplicate=True),
    Input({"type": "remove-style-btn", "index": ALL}, "n_clicks"),
    State("user-plan", "data"),
    prevent_initial_call=True,
)
def _remove_style(_n_clicks_list, plan):
    triggered_id = ctx.triggered_id
    triggered_value = ctx.triggered[0]["value"] if ctx.triggered else None
    if not triggered_id or not triggered_value:
        return dash.no_update
    plan = dict(plan or {})
    ids = list(plan.get("selected_style_ids") or [])
    if triggered_id["index"] in ids:
        ids.remove(triggered_id["index"])
    plan["selected_style_ids"] = ids
    return plan


@callback(
    Output("user-plan", "data", allow_duplicate=True),
    Input({"type": "remove-product-btn", "index": ALL}, "n_clicks"),
    State("user-plan", "data"),
    prevent_initial_call=True,
)
def _remove_product(_n_clicks_list, plan):
    triggered_id = ctx.triggered_id
    triggered_value = ctx.triggered[0]["value"] if ctx.triggered else None
    if not triggered_id or not triggered_value:
        return dash.no_update
    plan = dict(plan or {})
    ids = list(plan.get("selected_product_ids") or [])
    if triggered_id["index"] in ids:
        ids.remove(triggered_id["index"])
    plan["selected_product_ids"] = ids
    return plan


def _usage_text(usage_total: dict) -> str:
    total_tokens = usage_total["input_tokens"] + usage_total["output_tokens"]
    if total_tokens == 0:
        return "No messages yet."
    return (
        f"Session usage: {total_tokens:,} tokens "
        f"({usage_total['input_tokens']:,} in / {usage_total['output_tokens']:,} out) "
        f"~ ${usage_total['cost_usd']:.4f} (gpt-6-luna)"
    )
