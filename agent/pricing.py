"""Token cost accounting for the one model this app uses.

Rate is USD per one million tokens, same figures used in the sibling
mult_agent_hp_tokenomics project (from the OpenAI API pricing page).
"""

from __future__ import annotations

from dataclasses import dataclass

MODEL_NAME = "gpt-6-luna"
INPUT_PER_MILLION = 0.20
CACHE_READ_PER_MILLION = 0.02
OUTPUT_PER_MILLION = 1.00


@dataclass(frozen=True)
class UsageSummary:
    input_tokens: int
    output_tokens: int
    cost_usd: float


def summarize_usage(usage) -> UsageSummary:
    input_tokens = max(int(getattr(usage, "input_tokens", 0) or 0), 0)
    cache_read_tokens = max(int(getattr(usage, "cache_read_tokens", 0) or 0), 0)
    output_tokens = max(int(getattr(usage, "output_tokens", 0) or 0), 0)
    regular_input_tokens = max(input_tokens - cache_read_tokens, 0)
    cost = (
        regular_input_tokens * INPUT_PER_MILLION
        + cache_read_tokens * CACHE_READ_PER_MILLION
        + output_tokens * OUTPUT_PER_MILLION
    ) / 1_000_000
    return UsageSummary(input_tokens=input_tokens, output_tokens=output_tokens, cost_usd=round(cost, 6))
