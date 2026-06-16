from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_effective_date_overlap_detector_identifies_active_mapping_conflict() -> None:
    result = subprocess.run(
        [sys.executable, "src/python/check_effective_date_overlap.py"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload == [
        {
            "dq_rule_id": "DQ_CTRL_001",
            "business_key": "location_to_zone",
            "source_value": "LOC-02",
            "first_mapping_id": "MAP_002",
            "second_mapping_id": "MAP_003",
            "first_window": "2026-01-01..2026-01-20",
            "second_window": "2026-01-15..2026-02-28",
        }
    ]


def test_effective_date_overlap_strict_mode_returns_nonzero() -> None:
    result = subprocess.run(
        [sys.executable, "src/python/check_effective_date_overlap.py", "--strict"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
