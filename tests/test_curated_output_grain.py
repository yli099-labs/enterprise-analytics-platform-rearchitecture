from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_curated_daily_visitorship_expected_output_has_stable_grain() -> None:
    rows = read_csv(REPO_ROOT / "samples/expected_output/curated_daily_visitorship.csv")
    grain = {(row["business_date"], row["analytics_entity_code"]) for row in rows}

    assert len(rows) == len(grain)
    assert grain == {
        ("2026-01-05", "ZONE-A"),
        ("2026-01-05", "ZONE-B"),
        ("2026-01-06", "ZONE-A"),
        ("2026-01-06", "ZONE-C"),
    }
    assert all(int(row["total_visitors"]) >= int(row["open_hours_visitors"]) for row in rows)


def test_file_registry_example_matches_current_sample_files(tmp_path: Path) -> None:
    generated = tmp_path / "file_registry_example.csv"
    subprocess.run(
        [
            sys.executable,
            "src/python/generate_file_registry.py",
            "--output",
            str(generated),
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    expected_rows = read_csv(REPO_ROOT / "samples/expected_output/file_registry_example.csv")
    generated_rows = read_csv(generated)

    assert expected_rows == generated_rows
    assert {row["schema_status"] for row in generated_rows} == {
        "contract_match",
        "drift_observed",
    }
