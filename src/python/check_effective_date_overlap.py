from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

from proof_utils import read_csv_rows


DEFAULT_MAPPING_FILE = Path("samples/input/manual_mapping_current.csv")


def parse_date(value: str) -> date:
    return date.max if value == "" else date.fromisoformat(value)


def find_overlaps(mapping_file: str | Path = DEFAULT_MAPPING_FILE) -> list[dict[str, str]]:
    rows = [row for row in read_csv_rows(mapping_file) if row["is_active"] == "Y"]
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["business_key"], row["source_value"])].append(row)

    overlaps: list[dict[str, str]] = []
    for (business_key, source_value), windows in grouped.items():
        ordered = sorted(windows, key=lambda row: row["effective_from"])
        for previous, current in zip(ordered, ordered[1:]):
            previous_end = parse_date(previous["effective_to"])
            current_start = date.fromisoformat(current["effective_from"])
            if current_start <= previous_end:
                overlaps.append(
                    {
                        "dq_rule_id": "DQ_CTRL_001",
                        "business_key": business_key,
                        "source_value": source_value,
                        "first_mapping_id": previous["mapping_id"],
                        "second_mapping_id": current["mapping_id"],
                        "first_window": f"{previous['effective_from']}..{previous['effective_to'] or 'open'}",
                        "second_window": f"{current['effective_from']}..{current['effective_to'] or 'open'}",
                    }
                )
    return overlaps


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping-file", default=str(DEFAULT_MAPPING_FILE))
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when active effective-date overlaps are found.",
    )
    args = parser.parse_args()

    overlaps = find_overlaps(Path(args.mapping_file))
    print(json.dumps(overlaps, indent=2))
    return 1 if args.strict and overlaps else 0


if __name__ == "__main__":
    raise SystemExit(main())
