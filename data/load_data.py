"""Load the project's CSV datasets with correct types and a couple of display helpers.

Run directly (`python data/load_data.py`) to sanity-check the files load cleanly.
"""
import csv
from pathlib import Path

DATA_DIR = Path(__file__).parent

# Values that mean "we don't have this fact" across the CSVs - never coerce these to 0 or "".
_UNKNOWN_VALUES = {"", "not confirmed", "not available", "not yet rated", "not specified"}


def _to_float(value):
    """Return a float, or None if the field is blank or an 'unknown' marker."""
    value = (value or "").strip()
    if value.lower() in _UNKNOWN_VALUES:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _to_int(value):
    value = (value or "").strip()
    if not value.isdigit():
        return None
    return int(value)


def load_csv(filename):
    """Read a CSV from data/ as a list of dicts. Always opened as UTF-8 so accented
    brand names (Cécred, Crème) read correctly regardless of the OS default encoding."""
    path = DATA_DIR / filename
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_providers():
    rows = load_csv("providers.csv")
    for row in rows:
        row["price_from_usd"] = _to_float(row["price_from_usd"])
        row["price_to_usd"] = _to_float(row["price_to_usd"])
        row["rating_value"] = _to_float(row["rating_value"])
        row["review_count"] = _to_int(row["review_count"])
        row["lat"] = _to_float(row.get("lat"))
        row["lon"] = _to_float(row.get("lon"))
    return rows


def load_products():
    rows = load_csv("products.csv")
    for row in rows:
        row["price_usd"] = _to_float(row["price_usd"])
    return rows


def product_service_paths(product_row):
    """A product's service_path field can hold multiple ';'-separated values
    when the same real product is genuinely useful across more than one style
    path (e.g. a scalp oil good for both braids and locs) - that's one row,
    not a duplicate per style. Always read service_path through this helper
    rather than comparing the raw field directly."""
    return [v.strip() for v in (product_row.get("service_path") or "").split(";") if v.strip()]


def load_care_guidance():
    return load_csv("care_guidance.csv")


def load_brand_candidates():
    return load_csv("product_brand_candidates.csv")


def price_display(provider_row):
    """Graceful price text for a provider card, even when no price was ever sourced
    (e.g. Joyce House of Beauty, NH09) - never show a blank or '$None'."""
    low = provider_row.get("price_from_usd")
    high = provider_row.get("price_to_usd")
    if low is None:
        return "Price not listed - contact the provider directly to ask"
    if high is not None and high != low:
        return f"${low:g}-${high:g}"
    return f"${low:g}+"


def wash_blowdry_badges(provider_row):
    """Confirmed wash/blow-dry status becomes a short badge. Skipped when the service
    name already says it (e.g. a service literally named "Wash and retwist") so the
    card doesn't repeat the same fact three times; skipped entirely (no placeholder
    text) when nothing is confirmed, to keep unpriced-info cards short."""
    badges = []
    service_name = (provider_row.get("service") or "").lower()
    wash = (provider_row.get("wash_status") or "").strip().lower()
    blowdry = (provider_row.get("blowdry_status") or "").strip().lower()
    if wash and wash not in _UNKNOWN_VALUES and "wash" not in service_name:
        badges.append("Wash included" if wash.startswith("included") else f"Wash: {wash}")
    if blowdry and blowdry not in _UNKNOWN_VALUES and "blow" not in service_name:
        badges.append("Blow-dry included" if blowdry.startswith("included") else f"Blow-dry: {blowdry}")
    return badges


if __name__ == "__main__":
    providers = load_providers()
    products = load_products()
    guidance = load_care_guidance()
    print(f"providers: {len(providers)} rows")
    print(f"products: {len(products)} rows")
    print(f"care_guidance: {len(guidance)} rows")

    # Spot-check the two display helpers against a priced row and the unpriced one (Joyce House of Beauty).
    for row in providers:
        if row["provider_id"] in ("NH01", "NH09"):
            print(row["provider_id"], row["public_business_name"], "->", price_display(row))
            print("   ", wash_blowdry_badges(row))
