# Harness

What the agent can actually touch: the data files, the tools that read/write
them, and the shared state that connects the chat to the other three pages.
For the full schema conventions, controlled vocabularies, and sourcing
methodology behind each file, see `data/README.md` - this is the shorter
"what's the operating surface" reference; that one is the deep "why is it
shaped this way" reference.

## Data files

### `data/providers.csv` - 76 rows, 10 New Haven-area businesses

Sourced stylist/salon listings. Key fields: `service_path` (one of
`box_knotless_braids`, `twists_plaits_cornrows`, `locs`), `price_from_usd`/
`price_to_usd`, `budget_tier` (`low`/`mid`/`high`, computed per business per
`service_path` - see `data/README.md`), `rating_platform`/`rating_value`/
`review_count` (kept per-platform, never averaged), `booking_url`, `lat`/
`lon`, `notes` (a sourcing audit trail for this project's own research, not
user-facing copy), `checked_at`.

### `data/products.csv` - 39 rows, 7 brands

Sourced product listings. Key fields: `service_path` (same three values,
`;`-separated when one product genuinely fits more than one), `product_type`
(`shampoo`/`conditioner`/`oil`/`gel`/`spray`/`moisturizer_cream`), `phase`
(`braid_preparation`/`braid_maintenance`/`natural_style_wash_styling`/
`takedown`), `price_usd`, `budget_tier`, `source_supported_claim` (a direct
quote from the product's own page - never paraphrased into a stronger
claim), `image_url`, `checked_at`.

### `data/care_guidance.csv` - 32 rows

Sourced before/during/after care steps, one per real dermatologist or AAD
source. Key fields: `service_path`, `phase` (same four values as products;
`pages/care_guide.py` maps these to its Before/During/After columns),
`plain_language_guidance`, `source_title`/`source_url`/`checked_at`,
`limits_or_uncertainty` (shown as a caveat whenever a source disagrees with
another or doesn't fully cover the style).

## Tools (`agent/tools_data.py`, `agent/planner.py`)

| Tool | Reads/writes | Used for |
|---|---|---|
| `search_providers(service_path, max_price_usd=None)` | `providers.csv` | Comparing real local stylists |
| `search_products(service_path=, phase=, budget_tier=, brand=, product_type=)` | `products.csv` | Recommending real products in budget |
| `search_care_guidance(service_path, phase=None)` | `care_guidance.csv` | Building a sourced prep/maintenance/takedown plan |
| `update_plan(field, value)` | `PlanState` (shared store) | Recording service_path/neighborhood/budget_tier/prep_time as the user states them |
| `modify_plan_selection(selection_type, item_id, action)` | `PlanState` (shared store) | Adding/removing a specific stylist or product from chat, mirroring the "Choose this stylist" / "Add to my plan" buttons |

All five are read-only over the CSVs except the last two, which only ever
write into the in-memory `PlanState` for the current session - never back to
the CSV files themselves.

## Shared state

`PlanState` (`agent/planner.py`) is serialized into a `dcc.Store(id="user-plan")`
at the Dash app-shell level (`app.py`), so `pages/providers_map.py`,
`pages/products_catalog.py`, and `pages/care_guide.py` all read the same
plan the chat agent builds, and can also write to it directly (e.g. clicking
"Add to my plan" on a product card).

## Audit trail

Every tool call is logged to `output/audit_trail.jsonl` (see `agent/audit.py`)
- one JSON object per line, with a `run_id` grouping every event in one chat
turn, a `step` counter, and `event_type` (`turn_start`, `tool_call`,
`turn_end`). This is what to point to for "the agent only acted on real tool
data" evidence - e.g. `tests/test_prompt_injection.py`'s run shows up here as
a normal `search_providers` call and nothing else, even with an injected
instruction sitting in the data it read.
