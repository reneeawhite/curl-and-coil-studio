"""Re-check reminder: scans every sourced row in data/ and flags any whose
checked_at date is more than data.load_data.STALE_AFTER_DAYS old.

This project's provider prices, ratings, and product claims are a snapshot,
not a live feed (see data/README.md) - nothing re-fetches a Booksy page or a
brand site automatically. Run this periodically (a maintainer's job, not the
app's) to see what's aged out and needs a human to re-check it against the
live source before it's trusted again.

Run it directly:
    .venv/bin/python3 scripts/check_data_freshness.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data.load_data import STALE_AFTER_DAYS, is_stale, load_care_guidance, load_products, load_providers


def _check(label, rows, id_field, name_field):
    stale = [r for r in rows if is_stale(r.get("checked_at"))]
    print(f"{label}: {len(rows)} rows, {len(stale)} stale (checked_at older than {STALE_AFTER_DAYS} days)")
    for r in stale:
        print(f"  - {r[id_field]} ({r[name_field]}): checked {r['checked_at']}")
    return len(stale)


def main():
    providers = load_providers()
    products = load_products()
    guidance = load_care_guidance()

    total_stale = 0
    total_stale += _check("providers.csv", providers, "provider_id", "public_business_name")
    total_stale += _check("products.csv", products, "product_id", "product_name")
    total_stale += _check("care_guidance.csv", guidance, "guidance_id", "source_title")

    print()
    if total_stale:
        print(f"RESULT: {total_stale} row(s) need a human re-check against their live source.")
        sys.exit(1)
    else:
        print("RESULT: nothing is stale yet - every row was checked within the last "
              f"{STALE_AFTER_DAYS} days.")


if __name__ == "__main__":
    main()
