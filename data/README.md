# Data folder conventions

This documents decisions made while building the CSVs that aren't visible from the files
themselves — the controlled vocabularies, bucketing rules, and fallback behavior the app
should rely on. Update this file if you change any of these.

## service_path (providers.csv, products.csv, care_guidance.csv)

In `products.csv` only, this field may hold more than one value, separated by `;` (e.g.
`box_knotless_braids;locs`), when the same real product is genuinely useful across more than
one style path - always read it through `data/load_data.py`'s `product_service_paths()` helper
rather than comparing the raw string, since every place that filters products by style
(`agent/tools_data.py`'s `search_products`, `pages/products_catalog.py`'s style dropdown) needs
membership-in-list, not equality. `providers.csv` and `care_guidance.csv` keep a single value
per row - a stylist offers one priced service per row, and a care-guidance step belongs to one
style path's routine, so there's no equivalent case for either of those files.

Three base values, shared across all three files as the join key:

- `box_knotless_braids` — box braids and knotless braids.
- `twists_plaits_cornrows` — twists, twist-outs, plaits, and cornrows: temporary styles with a
  wear-then-takedown cycle.
- `locs` — a long-term commitment maintained by ongoing retwisting rather than taken down and
  redone the way the other two paths are.

UPDATED 2026-10-25: split out of a single `protective_natural_hairstyles` category (itself
renamed from an earlier `twists_twist_outs` on 2026-10-24) at the project owner's request,
after the Care Guide's "During" column for that one category got long and mixed unrelated
content - wash-and-go/twist-out wash-day care (natural_style_wash_styling, G08-G14) doesn't
really apply to mature locs, and locs' own traction-alopecia/retwist-risk content (G18, G19)
doesn't belong next to it either. The split also sharpens Find a Stylist filtering - a user who
wants a loc specialist (e.g. Enriched Locs LLC) no longer has to wade through general twist/
braid providers to find one. Every row across all three files that was `protective_natural_hairstyles`
was individually reclassified by hand based on what the specific service/product/guidance row
actually is (e.g. "Loc retwist and wash" → `locs`, "Senegalese twist" → `twists_plaits_cornrows`),
not by any mechanical rule - check a specific row's own content if its category looks surprising.

Two rows have an ambiguous service that was force-assigned a single value for joining —
check their `notes` field before trusting the category blindly: `providers.csv` NH03 (braids
vs. twist) and NH09 (multi-style business with no priced menu).

UPDATED 2026-10-25: added 2 products tagged `locs` (AIA06L, AIA07) after the project owner
asked for real loc-moisturizing options, since none of the original five brands had a
dedicated loc product. Both are general curly-hair products already proven real elsewhere in
this catalog - since they're genuinely useful for multiple style paths at once (a castor oil
doesn't stop being useful for braids just because it's also good for locs), `AIA06L` was
initially added as its own duplicate row of `AIA06`, just re-tagged to `locs`; `AIA07` (As I Am
CocoShea Spray Moisturizer, $9.99, 4 fl oz) is sourced fresh from asiamnaturally.com's own
product page.

UPDATED 2026-10-25 (later same day): merged `AIA06L` back into `AIA06` after the project owner
pointed out the duplicate castor-oil listing was confusing when browsing all styles at once.
`AIA06` now carries `service_path = "box_knotless_braids;locs"` (see the multi-value note
above) instead of existing as two rows - this is the first product to use the multi-value
form; `AIA07` stays a single-`locs` row since the As I Am catalog doesn't otherwise sell that
spray for braids/twists specifically.

UPDATED 2026-10-25 (later same day): added a 6th product, `BB01` (Bronner Brothers Tropical
Roots Firm Locking Gel), as the one genuinely loc-dedicated product at the time - then removed
it later the same day at the project owner's request and replaced it with 6 products from
Made For Locs (`MFL01`-`MFL06`), a brand whose whole catalog is built around locs, rather than
a single product from a brand that otherwise doesn't serve this style path. Sourced via Made
For Locs' public Shopify `/products.json` endpoint (reliable structured data: title, variant
prices, images, full product-description HTML), not by scraping the rendered collection page
(the static HTML has no product data - the grid is JS-rendered). The 6 chosen products span a
full loc care routine: `MFL01`/`MFL02` (Black Charcoal Shampoo/Conditioner, $14.99 each, 8 fl
oz - wash day), `MFL03` (Conditioning Hair Oil, $9.99, 4 fl oz - between-wash scalp/strand
oil), `MFL04` (Vegan Growth Serum, Pineapple scent, $12.99, 4 oz - scalp treatment), `MFL05`
(Vegan Aloe Vera Soothing & Styling Gel, $12.99, 8.8 fl oz - retwist/styling hold), `MFL06`
(Vegan Oil Spray, Pineapple scent, $9.99, 4 fl oz - daily moisture seal). Each `source_
supported_claim` quotes the product's own official page text (`body_html` from the Shopify
feed), the same sourcing standard used for every other brand in this catalog. Two of these
products (Oil Spray, Growth Serum) are sold in multiple scent/size variants that share one
multi-bottle hero photo on the collection page; rather than use that group shot, each
variant's own per-variant image was pulled from the feed so the product photo shows a single
bottle matching the specific size/scent actually priced here, consistent with every other
product in this catalog.

UPDATED 2026-10-25 (later same day): removed `AIA02` (As I Am Curling Jelly Definer) at the
project owner's request and replaced it with `AIA08` (As I Am Rice Water, $8.99, 16 fl oz) - a
genuine water-based spray for refreshing moisture on day 2+ of a twist-out, rather than a
styling gel/jelly that was effectively a duplicate role next to `AIA04` (Twist Defining Cream).
The owner also asked whether gels exist across the other brands, since gels are how a style
gets maintained day-to-day, and whether those same brands sell a water-based refresher spray
too - both researched directly (official site `/products.json` endpoints) rather than invented,
with "no match" left out rather than forced:

- `PB06` PATTERN Curl Gel ($12.00, 3 fl oz) and `PB07` PATTERN Hydrating Mist ($10.00, 3 fl oz,
  `twists_plaits_cornrows;locs` - PATTERN's own site lists it under their loc-care guidance too).
- `CE06` CÉCRED Strong Hold Gel ($32.00, 5 fl oz) and `CE07` CÉCRED Scalp Refreshing Spray
  ($38.00, 5.7 fl oz, `box_knotless_braids;locs` - its own page says it works "without
  disturbing your extensions or protective style," which is exactly the box-braids/locs case).
  Note: `CE07`'s printed bottle label reads "5.7 FL OZ" even though the site's own variant name
  for that size is "8 fl oz" - the printed label was used as the more direct source, consistent
  with how every other product's size in this catalog is read off the product's own packaging.
- `CD05` Carol's Daughter Black Vanilla Moisture & Hold Jelly ($13.99, 12 oz) and `CD06`
  Carol's Daughter Hair Milk Refresher Spray ($11.99, 10 fl oz) - picked over Carol's Daughter's
  other gel (Coco Crème Curl Shaping Cream Gel) because the Jelly's "up to 72 hours of hold"
  framing matches "gels are for maintaining a style" more directly than a wash-day-only gel.
- `ME05` Mielle Organics Rosemary Mint Hair Strengthening Edge Gel ($6.99, 2 oz,
  `box_knotless_braids;twists_plaits_cornrows;locs` - an edge gel is useful regardless of what
  the rest of the hair is styled into). Mielle does not get a spray: the only real candidate
  found (Lavender & Lychee Scalp Soothing Daily Refresher) is a medicated Pyrithione Zinc
  dandruff treatment, not a plain moisture/curl refresher, so it was left out rather than
  force-fit into a role it isn't really for.

This research was originally delegated to a background subagent; the project owner asked that
it be done directly instead, so that agent was stopped mid-task. It had already written 5 rows
(`AIA08`, `PB06`, `CE06`, `CD05`, `ME05`) with different product picks/prices/claims before
being stopped - those stale rows were found and removed in favor of the versions sourced
directly afterward, documented above.

`PB06` and `PB07`'s official product photos (patternbeauty.com) are shot against PATTERN's own
yellow brand-color backdrop, which is close enough to the yellow bottle/tube color that the
corner-flood-fill algorithm (see the image-background section below) tunneled straight through
the product instead of just the background - the same failure class as the two-tone AIA photos
from earlier in this project, just via color proximity instead of a shadow gradient. Fixed by
sourcing alternate photos on plain white/neutral backgrounds instead: `PB06`'s photo is cropped
from a multi-product Amazon listing photo (isolating just the PATTERN tube, cutting out a
bundled Cantu sample packet, before running background removal) and `PB07`'s is cropped from a
hand-holding-the-bottle lifestyle photo (cropped to exclude as much of the hand as possible
without losing the "3 FL OZ" label line - a small fingertip is still visible at the bottom edge,
a minor cosmetic tradeoff preferred over a destroyed product or a mismatched-size photo).

UPDATED 2026-10-25 (later same day): fixed two more background artifacts the project owner
flagged by screenshot. `MFL05`'s official photo (madeforlocs.com) is shot on the same yellow
backdrop as the PB06/PB07 case above, but less uniformly lit - a soft lighting gradient near the
pump left a disconnected patch of yellow that the flood fill couldn't reach from any corner,
showing up as a jagged streak on an otherwise-white card. Fixed by using a different official
photo of the same product (madeforlocs.com lists several; one is a plain-white studio shot,
`MADEFORLOCSALOEVERASTYLINGGEL_5.jpg`) instead of trying to rescue the yellow-backdrop one.
`CE06` and `CE07` (Cécred gel and spray) looked "weird" per the owner because cecred.com's own
product photography is all moody campaign-style shots (dark gradients, stone pedestals, close-up
details) with no plain-background option at all - unlike `CE01`-`CE05`, which were sourced from
Ulta rather than Cécred's own site. Fixed the same way: `CE06`/`CE07` now use Ulta's own product
images (`media.ultainc.com`), which come as pre-cut transparent PNGs straight from the retailer -
no flood-fill needed at all, and visually consistent with every other Cécred card in this
catalog. Lesson carried forward: when a brand's own site has no clean product-only photography,
check where this catalog's *other* products from that brand were actually sourced before
reaching for background-removal workarounds.

## product_type (products.csv)

ADDED 2026-10-25: a controlled-vocabulary column for the Shop Products page's product-type
filter, separate from the free-text `category` field (which stays as the more specific,
human-written description like "hair oil (foam-to-oil)" or "scalp growth serum"). Six values:
`shampoo`, `conditioner`, `oil`, `gel`, `spray`, `moisturizer_cream`. Every row was assigned by
hand based on what the product actually is, not by mechanically parsing `category` text - a few
judgment calls worth noting:

- Co-washes (`AIA01`) are bucketed as `conditioner`, not `shampoo` - a co-wash is a cleansing
  conditioner, and retailers conventionally shelve it with conditioners despite the cleansing
  role.
- Leave-in lotions, leave-in moisturizers, and styling creams (`CE02`, `CD02`, `AIA04`, `PB03`)
  are `moisturizer_cream`, while leave-in *conditioners* (`PB01`, `AIA03`, `ME03`) stay
  `conditioner` - the product's own name is the signal here, since both are leave-in products
  applied to damp hair.
- Scalp growth serums (`MFL04`) are bucketed as `oil`, since it's an oil-based dropper
  treatment, not a spray or gel.
- Anything dispensed as a spray (`oil spray moisturizer`, `scalp spray`, `spray moisturizer`,
  `water-based spray`) is bucketed as `spray` regardless of what else is in the category name
  (e.g. `MFL06` "oil spray moisturizer" is `spray`, not `oil`) - the format of a product you'd
  actually filter for day-to-day is how it's dispensed, not just its ingredients.

UPDATED 2026-10-25 (later same day): added `AIA09` (As I Am Coconut Smoothing Gel, $8.00, 8 oz),
sourced directly from the project owner's own link to asiamnaturally.com/products/smoothing-gel.
Tagged `product_type = gel` and, since the product's own page describes it as being for
"smoothing the hairline or other areas of your 'do'" rather than any one style specifically,
`service_path = "box_knotless_braids;twists_plaits_cornrows;locs"` - the same reasoning as the
Mielle edge gel (`ME05`): a hairline/edge smoother is useful regardless of what the rest of the
hair is styled into.

## phase (products.csv, care_guidance.csv)

- `braid_preparation`, `braid_maintenance`, `takedown` — originally named for
  `box_knotless_braids`, but `braid_maintenance` and `takedown` are now reused as-is for
  `twists_plaits_cornrows` and `locs` rows too rather than inventing per-category phase names.
  The "braid_" prefix on `braid_maintenance` is a naming artifact from when only one service
  path existed — don't read it as braids-only.
- `natural_style_wash_styling` — under `twists_plaits_cornrows` and `locs` only (not
  `box_knotless_braids`).

UPDATED 2026-10-25: moved 3 existing `twists_plaits_cornrows` rows in `care_guidance.csv` to a
different `phase` after the project owner reviewed the live Before/During/After columns on the
Care Guide page and pointed out they were sitting in the wrong one - the guidance itself didn't
change, only which of the page's three columns it displays under (see `pages/care_guide.py`'s
`PHASE_TO_COLUMN` mapping):
- `G10` "Detangle wet, never dry": `natural_style_wash_styling` → `takedown`. Its own text
  describes detangling loose hair with a leave-in and a wide-tooth comb - the step that happens
  right after a twist/braid style comes out, before it's washed and redone, so "Taking it down"
  fits better than lumping it into the general wash-day column.
- `G12` "Protect hair from heat and sun": `natural_style_wash_styling` → `braid_preparation`.
  Its own text frames this as heat-protectant use "before any heat styling (such as stretching
  before a twist-out)" - that's prep done ahead of installing/restyling, not something done
  mid-wear.
- `G21` "Rest your scalp between protective styles": `braid_maintenance` → `takedown`. Its own
  text is explicitly about the gap *between* taking one style down and starting the next
  ("rather than going straight from one style into the next"), which is a takedown-adjacent
  decision, not something you do while the style is still in.

Row order within `care_guidance.csv` also sets display order within a column on the Care Guide
page (`_columns_for` doesn't re-sort - whatever order rows come out of the CSV is the order
cards render in), so the project owner also asked for two within-column reorders for a more
logical read: `G12` "Protect hair from heat and sun" now sits right after `G22` "Start with
clean, conditioned hair" in `braid_preparation` (wash/condition, then heat-protect, then the
stylist-pain note), and `G10` "Detangle wet, never dry" now sits right after `G20` "Take a style
down..." in `takedown` (decide to take it down, then detangle, then the scalp-rest note). Keep
this in mind when adding new rows - insert them at the file position where you want them to
appear, not just anywhere.

UPDATED 2026-10-25: the project owner noticed As I Am had no shampoo or conditioner under the
`natural_style_wash_styling` ("wash day") filter, even though every other brand in this catalog
does. Cause: `AIA01` (Coconut CoWash) and `AIA05` (Curl Clarity Shampoo) were only tagged
`box_knotless_braids` / `braid_preparation` ("pre-braid wash"), with no row covering the
twists/locs wash-day cycle at all. Fixed by retagging both to `twists_plaits_cornrows` /
`natural_style_wash_styling` instead of duplicating them into a second row - same reasoning as
the AIA06/AIA06L merge earlier (one real product, one row; pick the service path it's actually
missing rather than show it twice). This leaves `AIA03` (Leave-In Conditioner) as the sole
`box_knotless_braids` / `braid_preparation` item for As I Am, which matches the pattern every
other brand already has (exactly one braid-prep product each) rather than leaving a gap there.
Also moved `AIA07` (CocoShea Spray Moisturizer) from `natural_style_wash_styling` to
`braid_maintenance` - its own `usage_notes` already described it as "a between-wash moisture
spray," i.e. a maintenance product, not a wash-day one; the phase tag had simply been set wrong
when it was added.

## budget_tier (products.csv)

UPDATED 2026-10-25: computed from the actual price distribution of all products, split into
roughly equal-sized thirds (tertiles) rather than round numbers picked in advance. As of adding
`AIA09` (net +1 product), across 39 priced products (min $6.99, max $44.00):

- `low`: under $11.89 (13 products)
- `mid`: $11.89–$14.99 (13 products)
- `high`: $14.99 and up (13 products)

This split came from the 33rd/66th percentile prices ($11.89 / $14.99). It has been recomputed
each time products were added or removed (previously $11.89/$14.99 across 38, $11.99/$14.99
across 31, $11.99/$14.99 across 32, $11.99/$21.99 across 27, $12.00/$21.99 across 24, and
$12.50/$26.50 across 20) - recompute these cutoffs (and re-run the tier assignment) any time
products are added or
removed, since the thresholds are tied to this specific catalog, not an absolute sense of
"cheap" or "expensive." Products are priced in different sizes (e.g. a 1.7 oz oil vs. a 16 oz
co-wash), so this still doesn't reflect cost-per-use — only sticker price.

## budget_tier (providers.csv)

ADDED 2026-10-25: replaced the Find a Stylist page's old "Under $150/$200/$300" price filter,
which the project owner noticed never actually changed the results. Cause: that filter showed a
business's pin if *any* of its service rows was under the cap, and every business in this
dataset has an affordable entry-level service for box braids and twists - so every cap, even
the lowest, matched 100% of businesses for those two styles. It only showed any effect for locs,
where prices span much further ($75–$1,450).

Fix mirrors the products.csv `budget_tier` tertile method, but computed **per business per
service_path**, not one number per business - a first pass that averaged across everything a
business offers was tried and rejected before this file was updated, because it let one
expensive outlier service drag a business's *entire* rating up/down across styles it wasn't even
about (e.g. a single $1,450 loc-install line item would have tagged a business "high budget"
even for its unrelated, separately-priced box-braid services). Per-style avoids that: a business
can be `low` for box braids and `high` for locs at the same time, which is what the style filter
and budget filter actually get combined to ask for.

Method: group `providers.csv` rows by `(public_business_name, service_path)`, average
`price_from_usd` within each group, then take the 33rd/66th percentile *within each
service_path's own set of businesses* (not across all three combined, since a "low" loc price
and a "low" braid price are different dollar amounts). As of 2026-10-25, computed over the 9
box-braid, 7 twist, and 7 loc businesses with priced rows:

- `box_knotless_braids`: low under $127.50, high at/above $150.60 (9 businesses)
- `twists_plaits_cornrows`: low under $123.75, high at/above $130.50 (7 businesses)
- `locs`: low under $153.75, high at/above $180.00 (7 businesses)

Every row for a given `(business, service_path)` pair gets the same tier - recompute this (same
script pattern as the products tertile) any time `providers.csv` prices change or a provider is
added/removed. The Find a Stylist detail panel shows this tier as a badge per service card
(not once per business), since it can legitimately differ by style within one business.

## wash_status / blowdry_status (providers.csv)

Mostly `"not confirmed"` — almost no public listing states this explicitly. Treat a
confirmed value (`"included"`) as a bonus fact to display, not something to expect on every
row. `load_data.py`'s `wash_blowdry_badges()` returns the confirmed badges, but skips a badge
when the `service` name already says the same thing (e.g. a service literally named "Wash and
retwist only") so the UI doesn't state "wash" three times on one card; it returns an empty
list (not a placeholder) when nothing is confirmed, so cards with no wash/blow-dry info stay
short instead of showing "ask the stylist" on every single one.

## Missing price (providers.csv)

`load_data.py`'s `price_display()` returns a "contact the provider directly" string when
`price_from_usd` is `None`, instead of showing a blank or `$None` — written for Joyce House of
Beauty (formerly NH09), the one provider with no price anywhere on its public pages. That row
was later dropped entirely (see "dropped Joyce" below), so no current row actually exercises
this path, but the fallback is kept since a future provider could still lack a price.

## image_url (products.csv)

Added 2026-10-24 for the Shop Products page (Phase 4), reworked the same day once the project
owner asked for images to float on a transparent background instead of sitting in their own
white/colored box.

**Sourcing.** For each product, fetched the page at `official_product_url` (falling back to
`other_source_url`) with a browser-like User-Agent and read its own `og:image` meta tag - the
same image the retailer uses for social-media link previews, not a scraped `<img>` guess. Four
products (As I Am's Coconut CoWash, Twist Defining Cream, and Jamaican Black Castor Oil;
Mielle's Rosemary Mint Leave-In) are all on sallybeauty.com pages that render their product
image client-side via JavaScript, so no `og:image` tag exists in the static HTML. For the three
As I Am products, the project owner supplied the brand's own official product photos directly
(`research/products/*.webp`, matched to the right product by reading the text/branding printed
on each jar/bottle) - Jamaican Black Castor Oil's photo was swapped once more (still project-
owner-supplied) for a plain single-bottle shot, since the first version included a decorative
glass vial and capsule props alongside the actual bottle. For the fourth (Mielle's Rosemary
Mint Leave-In, ME03), the project owner supplied a plain-background retailer photo directly (an
`.avif` file, which Pillow opened and converted without issue) - every product now has a real
photo, none fall back to the bottle icon.

**Transparent backgrounds.** Every sourced image (local or fetched) is downloaded once and run
through a flood-fill background remover (`scratchpad` during development; final technique: seed
the four corners only, flood-fill outward through any pixel within a small color tolerance of a
corner color, set those pixels' alpha to 0) and saved as a local PNG under
`assets/products/<product_id>.png` - `image_url` now points at that local file, not the
original remote URL. Two more aggressive variants were tried and rejected while working on the
As I Am Coconut CoWash and Twist Defining Cream photos above (their original backdrops are
two-tone color-block studio sets, not a single flat color): comparing each pixel to its
already-cleared neighbor instead of a fixed corner color, and matching against every distinct
color found anywhere along the border instead of just the four corners. Both successfully
cleared more of the background, but both also tunneled through soft drop-shadow gradients into
the product itself on at least one photo, which is a worse failure than the one it fixes - the
corner-only version is deliberately conservative instead, accepting a secondary background
color block left in frame rather than risking the product. For these two specific photos a
secondary color block did get left in frame; rather than live with that, both were re-sourced
from a plain-background retailer photo instead (Target for the CoWash, Walmart for the Twist
Defining Cream) and reprocessed - same fix already used for five other products below. As I
Am's Jamaican Black Castor Oil photo, supplied directly by the project owner, already had a
plain background and needed no re-sourcing.

Five more products (PATTERN Moisture Milk, CÉCRED Moisture Sealing Lotion, CÉCRED Clarifying
Shampoo & Scalp Scrub, As I Am Curl Clarity Shampoo, plus the two above) originally resolved to
artistic brand-marketing photography instead of a plain studio shot (a gradient backdrop, a
two-tone color-block backdrop, or a hand holding the bottle) that no version of the flood-fill
can cleanly cut out - all were re-sourced from a plain-background retailer photo instead (Ulta
for three, Target for one, Walmart for two) before processing, rather than shipping a bad
cutout. `research/products/` holds the original higher-resolution source images for the three
As I Am products where the project owner supplied them directly, even though two of those three
were ultimately superseded by a retailer photo for the reason above.

Re-run the whole pipeline (re-fetch + re-process) if a product's `official_product_url`/
`other_source_url` changes, or if a new product is added; none of this is kept in sync
automatically. `pages/products_catalog.py` falls back to a flat bottle icon for any row with a
blank `image_url`, never a broken `<img>` or a guessed photo.

## lat / lon (providers.csv)

Added 2026-10-24 for the Find a Stylist map (Phase 3). Geocoded once from each business's
existing `public_address` using OpenStreetMap's free Nominatim API (no key needed). Re-run the
geocoding script if an address in `public_address` changes; it is not kept in sync
automatically.

UPDATED 2026-10-25: Divi's Beauty Empire originally had no public street address on file, so it
was pinned to the New Haven 06515 ZIP centroid as an approximation. The project owner found its
real address via Apple Maps (35 Colby Ct, New Haven, CT 06515) and all 10 of its rows were
updated to the real, street-level geocoded coordinates - it's no longer an approximation.
Enriched Locs LLC (NH14) is now the only remaining ZIP-centroid approximation in this file, for
the same reason (no public street address found).

The map's visual style (`pages/providers_map.py`'s `_build_map_figure()`, `layout.map.style`;
the actual recoloring happens in `assets/map_style.json` + `assets/map_style_apply.js`, see the
comments in both) recolors CARTO's free Positron basemap to this app's own cream/teal/
terracotta/mustard palette, replacing an earlier plain `"carto-voyager"` default chosen
2026-10-24 to match a reference image the project owner supplied - the custom recolor, added
2026-10-24 later the same session, matches the site's own palette exactly instead of a
generic travel-map color scheme.

## provider_id scheme (providers.csv)

`NH##` per business, with a letter suffix (`NH04B`, `NH04C`, ...) for additional services at
the same business. Not globally sequential — treat it as an opaque ID, not something to sort
or parse.

## Service coverage per business (updated 2026-10-24)

Each business in `providers.csv` offers far more services than are listed here — e.g. Divi's
Beauty Empire's own Booksy menu has 60+ priced line items. This file intentionally keeps a
curated representative sample per business (now 5-10 rows each, up from 1-3) rather than a
full scrape, chosen to cover the style families a user is likely to ask about: box/knotless
braids, Senegalese/Marley/kinky twists, cornrows, Fulani/lemonade braids, faux locs, and a
dedicated takedown/removal service where one exists (valuable since `care_guidance.csv`'s
takedown phase was otherwise hard to source - see G15-G17 below). The 2026-10-24 expansion
(provider_id suffixes `D` onward) was read directly from each business's full Booksy service
menu (PDF captures in `research/providers/`), not estimated or extrapolated from the smaller
original sample.

Trivia resolved in passing: a review on Finger's of Art's Booksy page and Divi's Beauty
Empire's own reviews both show "Kemi Ajasa" as a staffer/stylist name - this confirms Kemi
Ajasa works at Divi's Beauty Empire, settling the "NOTABLE" breadcrumb left in NH01's `notes`
field about a possible connection to the earlier-dropped NH08 record. No data change was
needed since Divi's Beauty Empire is already represented; this is just a closed loose end.

Hairitisbeauty (NH04E-NH04N, also added 2026-10-24) was expanded the same way, but from an
already-on-file source rather than a newly supplied one: `research/providers/
hairitisbeauty_styleseat_full.mhtml`, a full capture of its 64-service StyleSeat profile that
had only yielded 3 of those services (NH04B-D) when first processed. Re-extracting the whole
MHTML surfaced the missing style families (Senegalese/Marley/kinky/passion twists, cornrows,
Ghana braids, loc re-twist, dreadlocks, a men's box-braid variant). Most of these new rows
have no per-service StyleSeat rating (only `rating_platform`/`value`/`count` for the handful
the site attaches a sub-rating to) - left as `"not confirmed"` rather than reusing the
business's overall 4.7 (26 reviews), to avoid implying a rating is for that specific service.

Joyce House of Beauty (NH09) was **not** expanded - its only source,
`research/providers/joyce_house_of_beauty_facebook.pdf`, is a Facebook page with photos and a
scam-warning post but no service menu or prices anywhere on it (re-checked 2026-10-24, same
conclusion as the original pass). There's nothing further to source for this business without
a new capture (e.g. if it ever gets a Booksy/StyleSeat profile).

## 2026-10-24: dropped Joyce, added 5 more businesses (6 -> 10)

The project owner asked whether 6 providers was enough coverage and whether Joyce House of
Beauty (NH09) should stay, given it had no price, no rating sample, and no service menu to
show. NH09 was removed outright rather than kept as a placeholder pin.

To get to a rounder 10, Booksy's own "Braids & Locs near New Haven, CT" directory
(`https://booksy.com/en-us/s/braids-locs/15428_new-haven`) was fetched to find other real,
already-reviewed businesses rather than guessing or reusing a business already in the file.
Several listed businesses were deliberately excluded:
- **Zero-review businesses** (Braidingstylesss, Freestyle Braids Beauty, Adji Professional
  African Hair Braiding) - no social proof at all, which would undercut the "reputable
  provider" premise the project owner was checking.
- **Crowned By Cass** - the page explicitly says a stylist "specializes in braided styles" but
  lists no priced braid service under her name; its actual menu is weaves/wigs/color/makeup,
  not a protective-style specialist.
- **Businesses outside a reasonable New Haven radius** (Finesse and Kens Beauty Bar, both
  13-17 miles out in Bridgeport/Stratford) - out of scope for a "New Haven" tool.

The 5 added (NH10-NH14), all with a real Booksy rating and review count, confirmed directly
from their own profile pages:
- **Stylesbyneish** (534 State St, New Haven - 5.0, 162 reviews)
- **Salon C'est La Vie** (31 Lucy St, Woodbridge - 5.0, 152 reviews) - the richest menu of the
  five, comparable in breadth to Divi's Beauty Empire.
- **HairArt By Ranada** (265 Morse St, Hamden - 5.0, 41 reviews)
- **Femme Expressions** (954 Chapel St, New Haven - 5.0, 11 reviews) - Booksy categorizes this
  business as "brows-lashes," but its own profile does list real, separately-priced braid/twist
  services, confirmed by fetching the page directly rather than trusting the category label.
- **Enriched Locs LLC** (Hamden, no public street address - same ZIP-centroid approach as
  Divi's Beauty Empire) - a dedicated loc specialist, added to diversify the
  `protective_natural_hairstyles` options beyond twists/cornrows; its own page notes new
  installs are paused after 2026-03-01 for the stylist's planned maternity leave, carried into
  that row's `notes` field since it affects bookability.

Also added (NH10E, NH13E): Stylesbyneish and Femme Expressions both separately list a
standalone wash+blow-dry service (not bundled into a style price) - per the project owner's
request, these got their own rows (`"Simple wash (shampoo, condition, blow dry)"` and `"Wash
and Blow Dry (only)"`) rather than being left out just because they aren't a braid/twist/loc
style themselves. Assigned `service_path = box_knotless_braids` as a default bucket, the same
convention already used for other style-agnostic prep services like "Braid down" - there's no
third "general prep" category, and these aren't tied to one hairstyle family any more than the
other.

Checked every other business's source material for the same kind of standalone wash/blow-dry
listing (the project owner asked directly whether any were missing) and found three more real
ones, added the same way: Finger's of Art's `"Blow dry and wash only"` (NH05H, $63-$70),
Salon C'est La Vie's `"Shampoo blowdry"` (NH11J, $50), and HairArt By Ranada's `"Shampoo and
Blow dry"` (NH12F, $75 - a separate, cheaper line item from its existing `"Shampoo/Blow-dry &
Braid Down"` combo, NH12C). Confirmed by re-checking each business's own menu text: Divi's
Beauty Empire, Karima, Nappy Pleasures, and Hairitisbeauty have no genuine standalone
wash/blow-dry item (Hairitisbeauty only has wash bundled with another style/treatment, e.g.
"Wash + Roller Set") - nothing was added for those four, not an oversight.

## usage_notes / source_supported_claim (products.csv)

CLEANED 2026-10-24: both fields were originally written as research-audit trails first,
user-facing fact second - `usage_notes` mixed a genuinely useful usage sentence with internal
sourcing commentary ("cecred.com returned HTTP 429 to automated fetch this session..."), catalog-
curation reasoning ("Added so Pattern has a full shampoo+conditioner+leave-in+oil set..."), or
internal product-id cross-references ("brand recommends following with... (ME02)"); the Shop
Products detail panel would have shown all of that verbatim. This is the exact same mistake
the Find a Stylist page's `notes` field made (see "dropped Joyce" section above) - fixed the
same way, by trimming each row down to only the end-user-relevant sentence(s). A genuine trust
signal that happened to be buried in the audit text (e.g. "Rated 4.88 from 65 reviews on the
official page") was kept; the internal-process commentary was not. `source_supported_claim`
kept its direct brand-page quote but dropped "fetched directly" / "confirmed via a full saved
copy (PDF)... provided by the project owner" down to a plain "(Ulta product page)"-style
citation. Write any future row's `usage_notes` as the clean end-user sentence from the start -
put sourcing caveats in a researcher-only place if they need to be recorded at all, not in a
column this page reads directly.

## limits_or_uncertainty (care_guidance.csv)

CLEANED 2026-10-25 for the Care Guide page (Phase 5) - same fix as `providers.csv`'s `notes`
and `products.csv`'s `usage_notes` earlier this session: 12 of 25 rows (G08, G15-G25) had this
field written as a research-audit trail first, caveat second ("CONFIRMED (2026-10-24): the
project owner opened the live page directly and confirmed it is a reputable source (WebFetch
itself still could not reach it - TLS certificate error...)"), including internal
cross-references to other row IDs ("see G19-G21", "fills the gap flagged in G07"). Trimmed each
down to the genuinely useful caveat only - what the source does/doesn't say, not how this
project verified it. `pages/care_guide.py`'s `_guidance_card()` also skips rendering this field
entirely when it's blank or literally "None noted." (G10, G13), rather than showing an empty
caveat box.

G07 (`box_knotless_braids`/`takedown`, "AAD gives no step-by-step takedown procedure") is
excluded from the Care Guide page's display entirely (`EXCLUDED_FROM_DISPLAY` in
`pages/care_guide.py`), though it's kept in the CSV. Its `plain_language_guidance` is itself
meta-commentary about a sourcing gap, not actual user-facing guidance - and that exact gap is
already filled by G15-G17's real, dermatologist-sourced takedown procedure in the same
before/during/after column, so showing G07 alongside them would just surface an internal
research note next to the real answer.

UPDATED 2026-10-25: G30 (`locs`/`takedown`) was rewritten after the project owner pointed out
that its original wording ("take a style down when it starts to loosen or pull, not just by the
calendar") was reused from the twists/braids takedown signal and reads as routine style
refresh advice - which is misleading for locs, since locs don't loosen and get redone on a
cycle the way a twist or braid does. The revised version frames loc removal as something you'd
do for a real reason (a traction-alopecia signal, or a genuine decision to stop wearing locs),
not routine upkeep, and its `limits_or_uncertainty` now says plainly that no dermatologist
source in this file gives a loc-removal technique - combing locs out or cutting them off is
practical knowledge about the hair texture, not a sourced clinical claim, and is labeled as
such rather than presented as if it were. Also added G32 (`locs`/`braid_maintenance`, "Watch
the weight of your locs, not just tightness"), from the same Dina Strachan MD article already
used for G19-G21/G30/G31 - a second research pass over that same page (re-fetched directly,
not just WebSearch-summarized) found it also names loc *weight* as its own traction-alopecia
risk factor, separate from tightness, which none of the existing rows had captured yet.

## Encoding

`products.csv` and `product_brand_candidates.csv` contain accented characters (Cécred,
Crème) and are saved as UTF-8. `providers.csv` and `care_guidance.csv` currently have no
non-ASCII characters, but open all four as UTF-8 explicitly anyway (as `load_data.py` does)
so a future edit with an accented name doesn't break silently. Check any file's encoding
yourself with `file -I <filename>` in Terminal.

## Known gaps (updated 2026-10-24)

- `care_guidance.csv` now has a real takedown procedure (G15-G17), sourced from a named
  dermatologist at Baylor College of Medicine (Dr. Oyetewa Oyerinde) rather than AAD, since
  AAD itself never publishes step-by-step takedown instructions (see G07). WebFetch could
  never reach the page directly (a TLS certificate error on blogs.bcm.edu every attempt), but
  the project owner opened the live page themselves on 2026-10-24 and confirmed it's
  reputable — G15-G17 are marked CONFIRMED on that basis.
- No professional or academic source was found for a specific loc retwist/maintenance
  frequency, despite three search passes. The second tracked down a peer-reviewed citation
  (Haskin & Aguh, *J Am Acad Dermatol* 2016;75(3):606-611 — see G18) that classifies locs as
  high-risk for traction alopecia but gives no retwist interval in any version of the text
  accessible (PubMed and Europe PMC both blocked automated fetch). The third found a
  board-certified dermatologist's own practice blog (Dr. Dina Strachan, FAAD — see G19-G21,
  fetched directly with no access issues) who explicitly states "no validated number" exists
  for protective-style duration and recommends an individualized interval from a
  dermatologist instead. That's useful: it confirms the gap is real, not just something this
  project failed to find. Only salon and product-blog sources give a specific number
  (commonly "every 4-8 weeks" depending on loc age), and research_checklist.md's standard
  excludes those — the project owner has decided to leave the specific-interval gap open.
  `protective_natural_hairstyles` now has general maintenance/takedown principles (G18-G21:
  keep retwisting loose, judge takedown by feel/appearance not just a calendar date, rest
  between styles) even without a specific-interval number.
- `care_guidance.csv` G08 now presents AAD's wash-frequency guidance as a range (about 1 to 3
  weeks) rather than picking one page's number, since the AAD's "Black hair" page says
  weekly/every-other-week and its "Curly hair" page says every 2-3 weeks. This is a synthesis
  of both pages' figures, not a published AAD recommendation in itself — see G08's
  `limits_or_uncertainty`.
- UPDATED 2026-10-24: `protective_natural_hairstyles` previously had almost no sourced content
  for `braid_preparation` (before) or `braid_maintenance` (during) — nearly everything was
  wash-day (`natural_style_wash_styling`) or takedown-adjacent. A targeted search for
  twist-specific prep/maintenance guidance found no dermatologist or academic source (only
  salon/blog content, excluded by this project's sourcing standard). Rather than leave the
  gap or pad every chat answer with "no sourced info" disclaimers, G22-G25 extend four
  already-verified AAD pages (same sources as the box_knotless_braids equivalents, G01-G04) -
  those pages discuss tension-related hair damage generally (tight ponytails, braids, locs,
  twists), not braids exclusively, so reusing them for twists is a reasonable extension, not a
  guess. Each row's `limits_or_uncertainty` says so explicitly.
