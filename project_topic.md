# Project Topic: Textured Hair Care Planning for Busy Clients

## Topic in one sentence

This project explores how an AI-assisted service can help busy people with curly or coily hair find a suitable local stylist and prepare for, maintain, and care for a style with less searching and uncertainty.

## The context

Hair care for textured hair can involve several connected tasks. Depending on the person, hair length and condition, and chosen style, a wash-and-style routine may include taking down a previous style, detangling, shampooing, conditioning or deep conditioning, stretching or blow-drying, and creating the next style. Protective styles such as box or knotless braids also require preparation and ongoing care. Natural styles such as twists and twist-outs involve their own preparation, styling products, and maintenance.

The time needed for these steps can be difficult to fit around classes, work, commuting, family obligations, and social commitments. The project is motivated by the concern that some people end up giving up sleep or recovery time to complete their hair routine. This is a problem statement drawn from the project owner's experience and observations. The project should validate how common it is, and how much time different routines take, through conversations with intended users rather than assuming every person has the same experience.

Hair is also personal and culturally meaningful for many Black people. Choosing a stylist can therefore involve more than finding an open appointment: clients may want confidence that a provider knows how to work with textured hair, respects the client's goals, and can deliver the service shown in their portfolio. The available information can be spread across booking pages, reviews, websites, and social media accounts. Comparing services, prices, wash and blow-dry details, and examples of completed work may take additional time.

## The problem the project addresses

The project focuses on two related forms of work that clients currently may have to do themselves:

1. **Finding and comparing a stylist.** A client needs to identify local providers who offer the desired textured-hair service, understand what is included in the listed price, compare public ratings and reviews, and find current booking or contact information.
2. **Planning care around the service.** A client needs to understand what to do before the appointment, which preparation tasks the stylist performs, what products might be useful within the client's budget, and how to maintain or eventually remove the style.

These tasks are connected. For example, whether a braid appointment includes washing and blow-drying can change both the time the client needs before the visit and the products they need to buy. The expected length of a style and its maintenance routine can also affect the total cost and effort of choosing it.

## Intended users and setting

The initial audience is people in the New Haven area who self-identify as having type 3B–4C curly or coily hair and want help choosing between textured-hair services. The project especially considers students and working professionals with limited discretionary time, since that is the context emphasized in the problem statement.

The app should not assume that every Black person has the same hair, needs, preferences, or budget. Users should be able to describe only the attributes they know and skip the rest. Curl pattern is one description of hair, not a complete assessment of what routine or product will work for someone.

## Proposed first experience

The initial service area is New Haven, Connecticut. The first service paths are:

- Box or knotless braids.
- Natural styles, starting with twists and twist-outs.

The user can choose a service, time available for preparation, product budget, and optional self-described attributes such as curl pattern, strand diameter, density, porosity, scalp profile, and elasticity. These attributes are optional inputs, not a diagnosis or a requirement for receiving help.

The app then supports a client through four stages:

1. **Compare local options.** Show a small, source-checked set of stylists who publicly list the selected service. Present service prices, wash and blow-dry information when available, ratings with their platform and review count, and links to booking or public portfolios. Each fact that can change should have a source and a checked date.
2. **Prepare for the appointment.** Explain the preparation steps associated with the selected service. Make clear which steps are the client's responsibility and which are included by the provider when that information is available.
3. **Choose products.** Recommend a small number of sourced products that fit the selected service, the user's stated needs, and their budget. Explain what role each product has in the plan and why it was selected. Brand popularity alone is not evidence that a specific item suits a specific person.
4. **Maintain the style.** Offer a service-specific care schedule and a reasonable check-in or takedown window when supported by the sources. Braid guidance and natural-style guidance should remain distinct because the styles have different care routines.

The first product research candidates are Pattern, Cécred, As I Am, and Carol's Daughter. They are candidate brands, not endorsements. Individual items, current prices, ingredients, and product claims still need verification.

## Why this may help

The intended benefit is to reduce the effort required to make a confident, informed decision. Instead of repeatedly moving among search results, booking sites, review platforms, and social profiles, a client could compare a focused set of local options and leave with a practical plan for the style they are considering.

The product and care-planning functions add value beyond a basic provider directory. They connect the appointment choice to the time and products needed before and after the service. The project should evaluate this benefit with intended users by measuring tasks such as time to compare options, whether users can find the information they need, how confident they feel in a choice, and whether the plan and product explanations are useful.

## How the idea relates to StyleSeat

StyleSeat is a relevant comparison because the project idea includes provider discovery, service menus, prices, ratings, and booking links. Those marketplace functions may overlap. The proposed distinction is a textured-hair-focused care journey: surface service details that affect preparation and upkeep, then connect the selected style to a personalized, source-backed routine and product suggestions.

The project should not claim that StyleSeat lacks any particular feature until its current pages and other relevant services have been checked. The report should compare concrete workflows and features, then explain what this project does differently and why that difference matters to its intended users.

## The role of AI

The app can use an AI agent to interpret the user's service and optional profile inputs, retrieve matching provider and product records from a small curated dataset, and explain a care plan using retrieved guidance. Structured tools can keep search and matching grounded in the recorded data. The agent should clearly say when a price, service detail, product fact, or appointment time is unknown instead of filling the gap with a guess.

The AI is not a hair diagnosis system and should not promise a particular product result. The client remains in control of the final choice and books through the provider's own contact or booking channel. Public provider and product descriptions should be treated as information to evaluate, not as instructions to the agent.

## Evidence the project should gather

Before making broad impact claims, the project should gather a small amount of direct evidence:

- Ask a few intended users how they currently find textured-hair stylists and compare prices or service details.
- Ask how they prepare for and maintain braids or natural styles, and where they currently get product recommendations.
- Have users complete a realistic provider-comparison and care-planning task with the prototype.
- Record task completion, time, questions users could not answer, confidence, and feedback on whether the product explanations make sense.
- Measure token use and estimated model cost from actual app runs. Distinguish measured values from projections to larger usage.

These steps can support a credible early evaluation. A small usability test does not establish that the app improves hair health or represents every textured-hair client's needs.

## Scope and limits for the first version

To make the project feasible, the first version should cover New Haven, the two selected service paths, a small set of publicly documented stylists, and a compact product catalog. Information should include source links and checked dates. A link to a provider's booking page is more reliable than presenting an in-app calendar as live when availability is not connected to a current booking system.

The first version should prioritize accurate service and care information over complete geographic coverage. It should not infer that a provider is qualified from photos alone, combine ratings from different platforms, invent prices or availability, or make medical claims. Care instructions and product claims should be tied to sources, and uncertainty should be visible.

## Working project description

> For busy people with curly or coily hair in New Haven, this project builds an AI-assisted textured-hair planner that compares a small set of local braid and natural-style providers, then creates a source-backed preparation and care plan with product suggestions that respect the user's needs and budget.

This description is a working scope. User interviews, provider research, product research, and a competitor review will determine which claims can be made confidently in the final report.
