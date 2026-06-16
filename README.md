# Enterprise DWH Re-Architecture & AI-Ready Analytics Platform

This public-safe case study describes the redesign of a legacy analytical warehouse from a brittle batch-reporting estate into a governed, explainable, and AI-ready data platform.

The project was not only a database migration or performance tuning exercise. The core challenge was architectural: ingestion, transformation procedures, historical retention, business rules, orchestration, and BI semantics had become tightly coupled. Runtime issues and recurring pipeline failures were symptoms of deeper design debt.

The redesign introduced a layered operating model, lifecycle-aware processing, clearer curated grains, source prioritization, governed rule history, stronger failure boundaries, and AI-readable metadata patterns.

This repository is intentionally not a fake production system. It is a public-safe architecture case study supported by representative implementation patterns using synthetic data.

## Five-Minute Review Path

1. Read [Problem Statement](docs/01_problem_statement.md).
2. Read [Legacy Estate Diagnosis](docs/02_legacy_estate_diagnosis.md).
3. Read [Target Architecture](docs/03_target_architecture.md).
4. Review the [architecture diagram](diagrams/architecture_layers.mmd).
5. Read [Trade-Offs](docs/09_tradeoffs.md).
6. Read [AI-Ready Layer](docs/08_ai_ready_layer.md).
7. Review the [implementation roadmap](docs/10_implementation_roadmap.md).
8. Run the lightweight proof layer below.

## Lightweight Proof Layer

The repository now includes a thin evidence pack so the architecture is supported by executable examples:

- synthetic inputs and expected outputs under [samples](samples/);
- source contracts, DQ rules, semantic definitions, and lineage metadata under [metadata](metadata/);
- representative SQL patterns under [src/sql](src/sql/);
- small Python validators under [src/python](src/python/);
- pytest checks under [tests](tests/).

Run from the repository root:

```bash
python -m pip install -r requirements.txt
python src/python/validate_source_contract.py
python src/python/detect_schema_drift.py
python src/python/check_effective_date_overlap.py
python src/python/generate_file_registry.py --output samples/expected_output/file_registry_example.csv
pytest
```

The scripts are deliberately small. They prove that contracts, schema drift, file registry evidence, effective-date rule validation, and curated-output grain checks can be operationalized without turning this case study into a full synthetic warehouse product.

## Evidence Map

| Claim | Evidence |
| --- | --- |
| Source contracts are explicit | [metadata/source_contracts](metadata/source_contracts/) |
| Schema drift is observable | [src/python/detect_schema_drift.py](src/python/detect_schema_drift.py) and [samples/input/survey_response_v2_schema_changed.csv](samples/input/survey_response_v2_schema_changed.csv) |
| Manual rules are history-managed | [src/sql/04_ctrl_rule_history_scd2.sql](src/sql/04_ctrl_rule_history_scd2.sql) and [samples/expected_output/rule_history_example.csv](samples/expected_output/rule_history_example.csv) |
| Curated outputs have stable grain | [src/sql/05_curated_daily_visitorship.sql](src/sql/05_curated_daily_visitorship.sql) and [tests/test_curated_output_grain.py](tests/test_curated_output_grain.py) |
| DQ is executable | [metadata/dq_rules](metadata/dq_rules/) and [tests](tests/) |
| AI-readiness is metadata-driven | [metadata/semantic_definitions](metadata/semantic_definitions/) and [metadata/lineage](metadata/lineage/) |
| File arrivals are controlled evidence | [src/python/generate_file_registry.py](src/python/generate_file_registry.py) and [samples/expected_output/file_registry_example.csv](samples/expected_output/file_registry_example.csv) |

## Story Spine

The legacy estate was not broken because it lacked pipelines. It was brittle because pipelines, historical data, business rules, procedures, and BI semantics were tightly coupled.

The redesign separated these responsibilities.

By applying lifecycle-aware processing, model rationalization, pipeline decoupling, source prioritization, and governed semantic outputs, the platform became faster, more reliable, easier to explain, and ready for future AI-assisted operations.

## Why This Is Not Just SQL Tuning

Query tuning can improve a slow procedure. It cannot fix an estate where:

- source behavior is learned from pipeline side effects instead of explicit contracts;
- old historical data is repeatedly touched by nightly jobs;
- transformation logic, business rules, audit evidence, and BI semantics live in the same procedural path;
- failures are hard to localize because steps are too coupled;
- report logic is repeated downstream because curated outputs are not stable enough;
- metadata and lineage are not explicit enough for AI-assisted operations.

The modernization therefore focused on architecture under constraint: define clearer boundaries, stop unnecessary work, make business meaning traceable, and expose trusted semantic outputs.

## Target Operating Model

```text
LANDING
  -> RAW evidence
  -> STG typed and standardized data
  -> CTRL registries, lifecycle, rules, DQ, lineage
  -> CUR governed facts, dimensions, and bridges
  -> SEM thin BI and semantic serving
```

Each layer has one job:

| Layer | Role |
| --- | --- |
| `LANDING` | Receive files, extracts, and manual-rule inputs without applying business interpretation. |
| `RAW` | Preserve source evidence with ingestion metadata for audit, replay, and traceability. |
| `STG` | Type, standardize, normalize, and prepare deterministic keys. |
| `CTRL` | Manage registries, rule history, data quality results, lineage, and lifecycle policy. |
| `CUR` | Publish governed facts, dimensions, bridges, and analysis-grade outputs. |
| `SEM` | Provide thin BI and semantic-serving views over curated data. |

## Key Design Decisions

| Decision | Why it mattered |
| --- | --- |
| Separate analytical refresh from historical retention | Reduced repeated scanning of stable history and made runtime improvement structural. |
| Move repeated rules into governed layers | Made business meaning reviewable, versioned, and easier to explain. |
| Keep raw evidence wide and curated outputs narrow | Preserved forensic value without leaking clutter or sensitive fields into BI. |
| Prioritize sources by analytical value | Prevented low-value or audit-only feeds from slowing the nightly analytical path. |
| Break opaque procedures into smaller responsibilities | Reduced failure scope and supported targeted replay or recompute. |
| Build metadata for AI after data controls | Allowed future assistants to explain lineage, DQ, schema drift, and rerun scope safely. |

## Outcome Framing

The platform runtime improved from multi-hour nightly processing toward a shorter controlled window because the architecture stopped doing unnecessary work, reduced redundant transformations, clarified model relationships, and separated analytical refresh from historical retention and audit-only data.

The more important result was reliability. The platform became less dependent on broad historical scans and large opaque procedures, reducing unknown timeout and stuck-step failure risk.

## Repository Guide

- [01 Problem Statement](docs/01_problem_statement.md) - why the platform needed architecture redesign, not more pipeline code.
- [02 Legacy Estate Diagnosis](docs/02_legacy_estate_diagnosis.md) - the symptoms, deeper root causes, and operational risks.
- [03 Target Architecture](docs/03_target_architecture.md) - the layer model and responsibility boundaries.
- [04 Data Lifecycle Strategy](docs/04_data_lifecycle_strategy.md) - hot/cold separation, targeted recompute, and source prioritization.
- [05 Model Rationalization](docs/05_model_rationalization.md) - curated grains, semantic outputs, and reducing redundant objects.
- [06 Pipeline Decoupling](docs/06_pipeline_decoupling.md) - failure-boundary reduction and replay design.
- [07 Governance and DQ](docs/07_governance_and_dq.md) - contracts, rule history, quality checks, and lineage.
- [08 AI-Ready Layer](docs/08_ai_ready_layer.md) - metadata foundation for safe AI-assisted data operations.
- [09 Trade-Offs](docs/09_tradeoffs.md) - practical choices and constraints.
- [10 Implementation Roadmap](docs/10_implementation_roadmap.md) - phased delivery plan.
- [Diagrams](diagrams/) - Mermaid diagrams for the architecture and operating model.
- [Assets](assets/) - public-safe templates for contracts, semantic outputs, DQ rules, and lifecycle policy.
- [Metadata](metadata/) - concrete source contracts, DQ rules, lineage, and semantic definitions.
- [Samples](samples/) - synthetic input and expected output examples.
- [SQL Patterns](src/sql/) - representative public-safe implementation patterns.
- [Python Validators](src/python/) - lightweight executable proof scripts.
- [Tests](tests/) - pytest coverage for contract checks, drift detection, date-window DQ, and curated grain.

## Confidentiality Note

This repository is public-safe by design.

- It does not use real organization, team, person, source system, vendor, table, report, endpoint, network path, or file names.
- Exact production schemas, credentials, row counts, KPI values, and private business definitions are omitted or generalized.
- Examples use logical labels such as `Source A`, `Rule Set B`, `CUR_FACT_X`, and `SEM_VIEW_Y`.
- The materials describe architecture patterns and decision logic, not copied production implementation code.

## Implementation Boundary

The production implementation was delivered by a team. This repository represents architecture and solution-design contribution: target-state design, data lifecycle strategy, model rationalization, governance patterns, semantic serving design, and AI-ready metadata thinking.

The artifacts are intentionally synthetic and public-safe. They are written for reviewers who need to understand the system design, not for operators to run a production platform.
