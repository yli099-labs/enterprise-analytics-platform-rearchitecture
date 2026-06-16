from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_schema_drift_detector_finds_changed_survey_workbook_shape() -> None:
    result = subprocess.run(
        [sys.executable, "src/python/detect_schema_drift.py"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = {
        item["sample_file"]: item
        for item in json.loads(result.stdout)
    }

    baseline = payload["samples/input/survey_response_v1.csv"]
    changed = payload["samples/input/survey_response_v2_schema_changed.csv"]

    assert baseline["status"] == "contract_match"
    assert changed["status"] == "drift_observed"
    assert changed["missing_required"] == ["satisfaction_score"]
    assert set(changed["unexpected_columns"]) == {"channel", "score_value"}


def test_schema_drift_strict_mode_returns_nonzero_for_drift() -> None:
    result = subprocess.run(
        [sys.executable, "src/python/detect_schema_drift.py", "--strict"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert "survey_response_v2_schema_changed.csv" in result.stdout
