"""MARB verification plan utilities with flexible export options."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import pandas as pd
import yaml


_PLAN_ROWS = [
    {
        "ID": 0,
        "Design Requirement": "MRB0 Reset default state",
        "Coverage": "cg_reset",
        "Verification Criteria": "Reset assertions + reg predictor mirror compare",
        "Priority": "High",
        "Type": "Design",
        "Comment": "Verify clean idle before enabling arbitration",
    },
    {
        "ID": 1,
        "Design Requirement": "MRB1 APB register access semantics",
        "Coverage": "APB addr/strb coverpoints",
        "Verification Criteria": "APB protocol checker + reg model sequences",
        "Priority": "High",
        "Type": "Protocol",
        "Comment": "Includes ready/slverr response on legal accesses",
    },
    {
        "ID": 2,
        "Design Requirement": "MRB2 Control enable gating",
        "Coverage": "ctrl_en toggle × request hit",
        "Verification Criteria": "Scoreboard blocks m_rd/m_wr when EN=0",
        "Priority": "High",
        "Type": "Design",
        "Comment": "Exercise enable transitions mid-traffic",
    },
    {
        "ID": 3,
        "Design Requirement": "MRB3 Static priority arbitration",
        "Coverage": "Priority order covergroup",
        "Verification Criteria": "Reference-model compares served client order",
        "Priority": "High",
        "Type": "Design",
        "Comment": "Expect fixed order (C0>C1>C2) under contention",
    },
    {
        "ID": 4,
        "Design Requirement": "MRB4 Round-robin / fairness mode",
        "Coverage": "Rotation-length coverpoint",
        "Verification Criteria": "Temporal checker ensures no starvation",
        "Priority": "High",
        "Type": "Design",
        "Comment": "Configure mode to rotating scheme, stress long bursts",
    },
    {
        "ID": 5,
        "Design Requirement": "MRB5 Dynamic priority register updates",
        "Coverage": "dprio value bins × strobes",
        "Verification Criteria": "Checker on priority_sel outputs post-write",
        "Priority": "Medium",
        "Type": "Design",
        "Comment": "Include partial writes and byte strobes",
    },
    {
        "ID": 6,
        "Design Requirement": "MRB6 Request/ack handshake integrity",
        "Coverage": "cg_req_ack latency cross",
        "Verification Criteria": "SDT assertions ensure single ack per request",
        "Priority": "High",
        "Type": "Protocol",
        "Comment": "Leverage SDT monitors for per-client timing",
    },
    {
        "ID": 7,
        "Design Requirement": "MRB7 Read data routing accuracy",
        "Coverage": "Read access × addr bins",
        "Verification Criteria": "Reference memory compares c*_rd_data",
        "Priority": "High",
        "Type": "Design",
        "Comment": "Covers data return for all clients and modes",
    },
    {
        "ID": 8,
        "Design Requirement": "MRB8 Write forwarding and strobes",
        "Coverage": "Write client × strb pattern",
        "Verification Criteria": "Scoreboard checks m_* matches issuing client",
        "Priority": "High",
        "Type": "Design",
        "Comment": "Exercise misaligned and byte-enable cases",
    },
    {
        "ID": 9,
        "Design Requirement": "MRB9 Back-to-back and overlapping traffic",
        "Coverage": "Burst length × concurrency",
        "Verification Criteria": "Sequence checker ensures queue depth preserved",
        "Priority": "Medium",
        "Type": "Design",
        "Comment": "Drive long random streams with zero idle cycles",
    },
    {
        "ID": 10,
        "Design Requirement": "MRB10 Invalid config/address handling",
        "Coverage": "cg_slverr illegal bins",
        "Verification Criteria": "APB checker expects slverr and no state change",
        "Priority": "Medium",
        "Type": "Protocol",
        "Comment": "Sweep out-of-range addresses and reserved bits",
    },
    {
        "ID": 11,
        "Design Requirement": "MRB11 Idle stability signaling",
        "Coverage": "Idle stable flag bins",
        "Verification Criteria": "Assertion holds m_* steady when stable=1",
        "Priority": "Low",
        "Type": "Design",
        "Comment": "Confirms quiescent behaviour for power-down",
    },
]


def get_marb_verification_plan() -> pd.DataFrame:
    """Return the MARB verification plan as a pandas DataFrame."""

    return pd.DataFrame(_PLAN_ROWS)


def _format_markdown(df: pd.DataFrame) -> str:
    try:
        return df.to_markdown(index=False)
    except (ImportError, AttributeError):
        return df.to_string(index=False)


def _format_yaml(records: Iterable[dict[str, object]]) -> str:
    return yaml.safe_dump(list(records), sort_keys=False)


def _format_json(records: Iterable[dict[str, object]]) -> str:
    return json.dumps(list(records), indent=2)


def format_marb_verification_plan(fmt: str) -> str:
    """Format the plan using *fmt* (markdown, markdow, yaml, or json)."""

    df = get_marb_verification_plan()
    records = df.to_dict(orient="records")

    formatters = {
        "yaml": lambda: _format_yaml(records),
        "json": lambda: _format_json(records),
        "markdown": lambda: _format_markdown(df),
        "markdow": lambda: _format_markdown(df),
    }

    try:
        return formatters[fmt]()
    except KeyError as exc:  # pragma: no cover - defensive guard
        raise ValueError(f"Unsupported format: {fmt}") from exc

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export MARB verification plan")
    parser.add_argument(
        "--format",
        choices=("yaml", "json", "markdown", "markdow"),
        default="yaml",
        help="Output format to generate (default: yaml)",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write the exported content",
    )
    return parser.parse_args()


def _write_output(content: str, fmt: str, path: Path | None) -> None:
    if path is None and fmt in {"markdown", "markdow"}:
        path = Path("marb_verification_plan.md")

    if path is None:
        print(content)
    else:
        path.write_text(content, encoding="utf-8")
        print(f"Saved {path} ({len(content)} bytes)")

def main() -> None:
    args = _parse_args()
    content = format_marb_verification_plan(args.format)
    _write_output(content, args.format, args.output)



if __name__ == "__main__":
    main()
