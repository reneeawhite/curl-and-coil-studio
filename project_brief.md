# Final Project Brief

## Working concept

Help busy people with type 3B–4C curly or coily hair in New Haven compare local stylists for braids or natural styles, then get a practical, source-backed preparation and care plan with product suggestions matched to their self-described needs and budget.

## The problem

Finding a stylist who understands textured hair can require searching scattered business pages and social accounts. Clients also need to understand service costs and preparation requirements, then fit detangling, washing, styling, and maintenance into a busy schedule. A useful solution should reduce search effort and make the before-and-after care clearer.

## Main differentiator

The care journey is central: connect the chosen salon service to a tailored preparation checklist, aftercare schedule, and a small set of explained product recommendations. Salon comparison helps the user get to that plan. The project should describe StyleSeat and other alternatives accurately and avoid claiming that no similar service exists without checking.

## Proposed MVP

1. Ask for a New Haven area or ZIP code, the desired service, available preparation time, product budget, and optional self-described hair attributes. Let users skip attributes they do not know. The first service paths are box/knotless braids and natural styles such as twists and twist-outs.
2. Search a small, curated set of local stylists. Show the service and sourced price, wash/blow-dry details when available, rating with review count and source, contact method, official booking page, and the date each detail was checked.
3. Build a service-specific plan with preparation steps, care cadence, and a suggested takedown/check-in window where relevant. Keep braid maintenance separate from natural-style maintenance. Explain uncertainty and link to the sources used.
4. Recommend a few products from a small, sourced catalogue. For each, show why it may fit the stated needs, how it is used in the plan, and a price/source with a checked date. Do not invent stock, prices, ingredients, or product effects.

Initial candidate brands named by the project owner: Pattern, Cécred, As I Am, and Carol's Daughter. These are leads for product research, not automatic endorsements; individual products still need source checks and should fit the selected service, stated needs, and budget.

Use one agent with focused tools for stylist lookup, product lookup, and retrieval of care guidance. Add multiple agents only if the chosen workflow demonstrates a real need for them.

## Scope controls

- Start with box/knotless braids plus twists/twist-outs and roughly 5–8 New Haven providers. Add other natural styles such as cornrows only if source coverage and time allow.
- Use verified public information in a compact local dataset, recording its source and last-checked date. Treat public listings as a snapshot, not a live or complete directory.
- Link to the stylist's booking system for current availability. Do not imply that an in-app calendar is live unless it is connected to a reliable source.
- Keep ratings attached to their named source and review count. Do not combine Apple and Google ratings into a single score.
- A simple provider list is the first milestone; an interactive map is a stretch feature if provider data and time allow.
- Keep hair attributes optional and self-reported. Hair pattern alone does not determine the right routine. Care guidance must be sourced, and the app must be clear when it cannot personalize a recommendation confidently.

## Evidence and evaluation

- Record sources and checked dates for salon details, product facts, prices, and care guidance.
- Test a few realistic user tasks with people who match the intended audience. Measure time to compare options, task completion, confidence, and whether the care plan and product rationale are understandable.
- Measure token usage and cost from actual runs. Keep a small test dataset with the app so it can run locally from a fresh clone.
- Test safety with misleading instructions embedded in a salon listing or product description; the agent should treat listings as data and never follow them as instructions.

## Decisions still needed

- Whether to include cornrows in the first natural-style menu.
- The minimum profile questions that meaningfully change the care plan or product suggestions.
- Which New Haven neighborhoods or ZIP codes to include in the initial dataset.
- Which real users can try the prototype and give feedback.
- Which specific products from the candidate brands have reliable product and price sources.

## Course constraints

- Due Monday, October 26, 2026 at 6:00 PM on Canvas.
- Course API key: use `PORTKEY_API_KEY` with `gpt-6-luna` only, per the assignment instructions.
- Keep API keys out of the repository. Include an `.env.example` and make the README work from a fresh clone.
- Required submissions: repo link, self-contained `report.html` that prints to 10–15 pages, and self-contained `slides.html` with at most 10 slides. A 2–3 minute demo video is optional.
