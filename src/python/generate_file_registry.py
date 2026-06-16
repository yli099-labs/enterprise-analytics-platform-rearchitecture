from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import TextIO

from proof_utils import all_contract_paths, csv_headers, csv_row_count, file_hash, hash_key, load_yaml, repo_path, schema_comparison


REGISTRY_FIELDS = [
    "registry_id",
    "source_name",
    "contract_id",
    "relative_path",
    "file_hash",
    "row_count",
    "column_count",
    "schema_status",
    "registered_at",
]


def build_registry_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    for contract_path in all_contract_paths():
        contract = load_yaml(contract_path)
        sample_files = [contract["sample_file"], *contract.get("drift_samples", [])]
        for sample_file in sample_files:
            relative_path = str(Path(sample_file)).replace("\\", "/")
            if relative_path in seen:
                continue
            seen.add(relative_path)
            comparison = schema_comparison(contract, sample_file)
            rows.append(
                {
                    "registry_id": "REG_" + hash_key(relative_path, file_hash(sample_file), length=10),
                    "source_name": contract["source_name"],
                    "contract_id": contract["contract_id"],
                    "relative_path": relative_path,
                    "file_hash": file_hash(sample_file),
                    "row_count": csv_row_count(sample_file),
                    "column_count": len(csv_headers(sample_file)),
                    "schema_status": comparison["status"],
                    "registered_at": "2026-06-16T00:00:00",
                }
            )
    return sorted(rows, key=lambda row: str(row["relative_path"]))


def write_registry(rows: list[dict[str, object]], handle: TextIO) -> None:
    writer = csv.DictWriter(handle, fieldnames=REGISTRY_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Optional output CSV path. Defaults to stdout.")
    args = parser.parse_args()

    rows = build_registry_rows()
    if args.output:
        output_path = repo_path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            write_registry(rows, handle)
    else:
        write_registry(rows, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
