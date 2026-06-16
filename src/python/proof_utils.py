from __future__ import annotations

import csv
import hashlib
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_DIR = REPO_ROOT / "metadata" / "source_contracts"


def repo_path(relative_path: str | Path) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def load_yaml(path: str | Path) -> dict[str, Any]:
    with repo_path(path).open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"YAML file did not contain a mapping: {path}")
    return data


def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    with repo_path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_headers(path: str | Path) -> list[str]:
    with repo_path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        return next(reader)


def csv_row_count(path: str | Path) -> int:
    return len(read_csv_rows(path))


def file_hash(path: str | Path, length: int = 16) -> str:
    payload = repo_path(path).read_bytes()
    return hashlib.sha256(payload).hexdigest()[:length].upper()


def hash_key(*parts: object, length: int = 16) -> str:
    payload = "|".join("" if part is None else str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:length].upper()


def all_contract_paths() -> list[Path]:
    return sorted(CONTRACT_DIR.glob("*.yml"))


def validate_scalar(value: str, expected_type: str) -> bool:
    if value == "":
        return False
    try:
        if expected_type == "string":
            return True
        if expected_type == "date":
            date.fromisoformat(value)
            return True
        if expected_type == "timestamp":
            datetime.fromisoformat(value)
            return True
        if expected_type == "integer":
            int(value)
            return True
        if expected_type == "decimal":
            Decimal(value)
            return True
    except (ValueError, InvalidOperation):
        return False
    raise ValueError(f"Unsupported expected type: {expected_type}")


def schema_comparison(contract: dict[str, Any], sample_file: str | Path) -> dict[str, object]:
    headers = set(csv_headers(sample_file))
    required = set(contract.get("required_columns", []))
    optional = set(contract.get("optional_columns", []))
    known = required | optional
    missing_required = sorted(required - headers)
    unexpected_columns = sorted(headers - known)
    status = "contract_match"
    if missing_required or unexpected_columns:
        status = "drift_observed"
    return {
        "source_name": contract["source_name"],
        "contract_id": contract["contract_id"],
        "sample_file": str(sample_file).replace("\\", "/"),
        "status": status,
        "missing_required": missing_required,
        "unexpected_columns": unexpected_columns,
    }
