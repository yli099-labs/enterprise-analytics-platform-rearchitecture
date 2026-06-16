from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_source_contract_validator_passes_for_registered_samples() -> None:
    result = subprocess.run(
        [sys.executable, "src/python/validate_source_contract.py"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert {item["source_name"] for item in payload} == {
        "manual_mapping",
        "opening_hours",
        "sensor_counts",
        "survey_workbook",
        "transaction_events",
    }
    assert all(item["status"] == "pass" for item in payload)


def test_transaction_contract_exposes_duplicate_policy_without_failing_schema() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "src/python/validate_source_contract.py",
            "--contract",
            "metadata/source_contracts/transaction_feed_contract.yml",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)[0]
    assert payload["duplicate_keys_observed"] == ["EVT-1002|1"]
    assert payload["duplicate_policy"] == "latest_batch_wins"
