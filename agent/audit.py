"""Structured audit log of every tool call the agent makes during a chat
turn - append-only JSON Lines at output/audit_trail.jsonl, one event per
line. Mirrors the audit_trail.json pattern from this course's earlier
homeworks, adapted to a long-running Dash app that handles many separate
chat turns rather than one batch run.

run_turn() in planner.py calls start_run() once per turn; every tool in
tools_data.py and planner.py then calls log_tool_call(). The result is a
real, inspectable record of what the agent actually looked up before
replying - useful for debugging, and as direct safety/agent-design evidence
(e.g. the prompt-injection test in tests/ produces a trace here showing the
agent called search_providers normally and never "did" anything else).
"""

from __future__ import annotations

import json
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
AUDIT_PATH = OUTPUT_DIR / "audit_trail.jsonl"

_run_state: ContextVar[dict | None] = ContextVar("_run_state", default=None)


def start_run(user_message: str) -> str:
    """Call once at the start of a chat turn. Returns the new run_id."""
    run_id = str(uuid.uuid4())
    _run_state.set({"run_id": run_id, "step": 0})
    log_event("turn_start", {"user_message": user_message})
    return run_id


def end_run(reply: str) -> None:
    log_event("turn_end", {"reply_preview": reply[:200]})


def log_event(event_type: str, details: dict[str, Any]) -> None:
    state = _run_state.get()
    if state is None:
        # A tool ran outside of run_turn() (e.g. a standalone test script) -
        # still log it, just without a chat-turn grouping.
        state = {"run_id": "no-run", "step": 0}
    state["step"] += 1
    event = {
        "event_id": str(uuid.uuid4()),
        "time": datetime.now(timezone.utc).isoformat(),
        "run_id": state["run_id"],
        "step": state["step"],
        "event_type": event_type,
        "details": details,
    }
    with open(AUDIT_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, default=str) + "\n")


def log_tool_call(tool_name: str, args: dict[str, Any], result_count: int | None) -> None:
    log_event("tool_call", {"tool": tool_name, "args": args, "result_count": result_count})
