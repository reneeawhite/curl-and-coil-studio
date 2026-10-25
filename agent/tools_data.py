"""Filters over the sourced CSV datasets in data/, used as the agent's tools.

Keep these pure and synchronous - no network calls, no LLM calls. The agent
should only ever see provider/product/care facts that passed through here,
never a listing's raw text treated as instructions (see planner.py's prompt).
"""

from __future__ import annotations

from agent.audit import log_tool_call
from data.load_data import (
    load_care_guidance,
    load_products,
    load_providers,
    price_display,
    product_service_paths,
    wash_blowdry_badges,
)

VALID_SERVICE_PATHS = {"box_knotless_braids", "twists_plaits_cornrows", "locs"}


def search_providers(service_path: str, max_price_usd: float | None = None) -> list[dict]:
    """Find New Haven-area providers offering a service path, optionally under a max price.

    service_path must be one of: box_knotless_braids, twists_plaits_cornrows, locs.
    """
    rows = load_providers()
    results = []
    for row in rows:
        if row["service_path"] != service_path:
            continue
        price = row["price_from_usd"]
        if max_price_usd is not None and price is not None and price > max_price_usd:
            continue
        results.append(
            {
                "provider_id": row["provider_id"],
                "business_name": row["public_business_name"],
                "neighborhood": row["neighborhood"],
                "service": row["service"],
                "price": price_display(row),
                "wash_blowdry": wash_blowdry_badges(row),
                "rating_platform": row["rating_platform"],
                "rating_value": row["rating_value"],
                "review_count": row["review_count"],
                "booking_url": row["booking_url"],
                "website_url": row["website_url"],
                "instagram_url": row["instagram_url"],
                "checked_at": row["checked_at"],
                "caveats": row["notes"],
            }
        )
    log_tool_call("search_providers", {"service_path": service_path, "max_price_usd": max_price_usd}, len(results))
    return results


def search_products(
    service_path: str | None = None,
    phase: str | None = None,
    budget_tier: str | None = None,
    brand: str | None = None,
    product_type: str | None = None,
) -> list[dict]:
    """Find products, optionally filtered by service_path, phase, budget_tier (low/mid/high),
    brand, or product_type (shampoo, conditioner, oil, gel, spray, moisturizer_cream)."""
    rows = load_products()
    results = []
    for row in rows:
        if service_path and service_path not in product_service_paths(row):
            continue
        if phase and row["phase"] != phase:
            continue
        if budget_tier and row["budget_tier"] != budget_tier:
            continue
        if brand and brand.lower() not in row["brand"].lower():
            continue
        if product_type and row["product_type"] != product_type:
            continue
        results.append(
            {
                "product_id": row["product_id"],
                "brand": row["brand"],
                "product_name": row["product_name"],
                "category": row["category"],
                "product_type": row["product_type"],
                "phase": row["phase"],
                "target_need": row["target_need"],
                "price_usd": row["price_usd"],
                "size": row["size"],
                "budget_tier": row["budget_tier"],
                "product_url": row["official_product_url"] or row["other_source_url"],
                "checked_at": row["checked_at"],
                "evidence": row["source_supported_claim"],
            }
        )
    log_tool_call(
        "search_products",
        {
            "service_path": service_path,
            "phase": phase,
            "budget_tier": budget_tier,
            "brand": brand,
            "product_type": product_type,
        },
        len(results),
    )
    return results


def search_care_guidance(service_path: str, phase: str | None = None) -> list[dict]:
    """Find sourced care-plan steps for a service path, optionally filtered by phase."""
    rows = load_care_guidance()
    results = []
    for row in rows:
        if row["service_path"] != service_path:
            continue
        if phase and row["phase"] != phase:
            continue
        results.append(
            {
                "guidance_id": row["guidance_id"],
                "phase": row["phase"],
                "step": row["step"],
                "guidance": row["plain_language_guidance"],
                "source": row["source_title"],
                "source_url": row["source_url"],
                "checked_at": row["checked_at"],
                "limits": row["limits_or_uncertainty"],
            }
        )
    log_tool_call("search_care_guidance", {"service_path": service_path, "phase": phase}, len(results))
    return results
