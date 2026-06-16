from __future__ import annotations

import argparse
import json
from pathlib import Path

from proof_utils import load_yaml, repo_path, schema_comparison


DEFAULT_CONTRACT = Path("metadata/source_contracts/survey_workbook_contract.yml")


def analyze_contract(contract_path: str | Path = DEFAULT_CONTRACT) -> list[dict[str, object]]:
    contract = load_yaml(contract_path)
    samples = [contract["sample_file"], *contract.get("drift_samples", [])]
    return [schema_comparison(contract, sample) for sample in samples]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", default=str(DEFAULT_CONTRACT))
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when any provided sample differs from the contract.",
    )
    args = parser.parse_args()

    results = analyze_contract(Path(args.contract))
    print(json.dumps(results, indent=2))
    if args.strict and any(result["status"] != "contract_match" for result in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
