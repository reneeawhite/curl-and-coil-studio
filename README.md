# Curl & Coil Studio

A New Haven-area planner for people with type 3B-4C curly or coily hair choosing between
box/knotless braids and protective natural hairstyles (twists, twist-outs, plaits, locs). One
chat agent compares sourced local stylists, builds a prep/maintenance/takedown plan, and
recommends a few products within budget - see `project_brief.md` and `project_topic.md` for
the full project scope, and `data/README.md` for how the underlying dataset is organized.

## Setup (fresh clone)

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your Portkey key:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and set `PORTKEY_API_KEY`. `MODEL_NAME` (`gpt-6-luna`) and
   `PORTKEY_BASE_URL` already have the course defaults - only change them if you need to.
   The app also looks for `.env` in parent folders, so a class-wide `.env` one level up
   (e.g. at `AI Foundations/.env`) works without copying the key into this folder.

## Run

```bash
.venv/bin/python3 app.py
```

Then open http://127.0.0.1:8050 in a browser. The server runs with `debug=False` and
`use_reloader=False` on purpose - editing a file does not auto-restart it, so stop the process
(Ctrl+C, or kill the whole process tree if it's running in the background) and start it again
to pick up changes.

## Project layout

- `app.py` - the Dash chat UI (Toca Boca Hair Salon theme).
- `agent/` - the single planning agent: `config.py` (Portkey/model setup), `pricing.py`
  (token cost accounting), `tools_data.py` (the three tools: provider, product, and
  care-guidance lookups over the CSVs), `planner.py` (the agent definition and system prompt).
- `data/` - the sourced CSV datasets (`providers.csv`, `products.csv`, `care_guidance.csv`,
  `product_brand_candidates.csv`), `load_data.py` (typed loader + display-fallback helpers),
  and `README.md` (schema conventions, known gaps, budget-tier methodology).
- `research/` - full-page captures (PDF/MHTML) used as primary evidence for CSV rows sourced
  from sites that blocked automated fetching - see `research/README.md`.

## Notes on the agent

- One agent, five tools, per the project brief's "use one agent with focused tools" direction:
  `search_providers`, `search_products`, and `search_care_guidance` (read-only lookups over the
  sourced CSVs), plus `update_plan` and `modify_plan_selection` (write the user's structured
  choices and specific stylist/product picks into the shared plan store that the other three
  pages read from).
- Every fact the agent states must come from a tool call in that conversation - the system
  prompt forbids inventing prices, ratings, ingredients, or availability, and requires
  carrying forward each fact's `checked_at` date and source.
- Listing and product text (business names, notes, descriptions) is treated as data, never
  as instructions, even if it reads like a command - this is a deliberate safety rule, since
  the dataset is scraped from public pages this app does not control.
- Session token usage and estimated cost are shown live at the bottom of the chat.
