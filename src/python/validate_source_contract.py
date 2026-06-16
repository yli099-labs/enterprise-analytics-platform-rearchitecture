from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from proof_utils import all_contract_paths, load_yaml, read_csv_rows, schema_comparison, validate_scalar


def validate_contract(contract_path: Path) -> dict[str, object]:
    contract = load_yaml(contract_path)
    sample_file = contract["sample_file"]
    rows = read_csv_rows(sample_file)
    schema = schema_comparison(contract, sample_file)
    issues: list[dict[str, object]] = []

    for column in schema["missing_required"]:
        issues.append(
            {
                "severity": "error",
                "rule_id": "DQ_STG_001",
                "column": column,
                "message": "Required column missing from sample file.",
            }
        )

    expected_types: dict[str, str] = contract.get("expected_types", {})
    for row_number, row in enumerate(rows, start=2):
        for column, expected_type in expected_types.items():
            if column in row and not validate_scalar(row[column], expected_type):
                issues.append(
                    {
                        "severity": "error",
                        "rule_id": "DQ_STG_002",
                        "row_number": row_number,
                        "column": column,
                        "detected_value": row[column],
                        "message": f"Value does not parse as {expected_type}.",
                    }
                )

    key_columns: list[str] = contract.get("key_columns", [])
    duplicate_keys: list[str] = []
    if key_columns and not schema["missing_required"]:
        keys = ["|".join(row[column] for column in key_columns) for row in rows]
        duplicate_keys = sorted(key for key, count in Counter(keys).items() if count > 1)

    return {
        "contract_id": contract["contract_id"],
        "source_name": contract["source_name"],
        "sample_file": sample_file,
        "status": "pass" if not issues else "fail",
        "row_count": len(rows),
        "duplicate_keys_observed": duplicate_keys,
        "duplicate_policy": contract.get("duplicate_policy"),
        "issues": issues,
    }


def validate_all(contract_paths: list[Path] | None = None) -> list[dict[str, object]]:
    paths = contract_paths or all_contract_paths()
    return [validate_contract(path) for path in paths]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contract",
        action="append",
        help="Optional source contract path. Can be passed more than once.",
    )
    args = parser.parse_args()

    paths = [Path(value) for value in args.contract] if args.contract else None
    results = validate_all(paths)
    print(json.dumps(results, indent=2))
    return 1 if any(result["status"] == "fail" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
