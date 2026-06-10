# 10. Implementation Roadmap

The roadmap is phased to reduce delivery risk. It does not assume the whole estate can be replaced at once.

## Phase 1: Discovery and Contract Baseline

Goals:

- inventory major source feeds, rule inputs, curated outputs, and BI dependencies;
- identify core analytical data versus audit-only data;
- define source owners and delivery patterns;
- document required columns, business dates, keys, and late-arrival behavior;
- classify high-risk procedures and report-side logic.

Deliverables:

- source contract backlog;
- legacy object classification;
- initial lineage sketch;
- prioritized domain list;
- implementation boundary and non-goals.

## Phase 2: Foundation Layers

Goals:

- establish `LANDING`, `RAW`, and `STG` conventions;
- preserve source evidence with ingestion metadata;
- standardize typing, date handling, and deterministic key patterns;
- add file and batch registries;
- introduce basic DQ checks before curated publication.

Deliverables:

- layer contracts;
- batch registry;
- schema registry pattern;
- idempotent load pattern;
- first DQ exception model.

## Phase 3: CTRL Layer and Rule Governance

Goals:

- move business rule handling into governed structures;
- add row-hash comparison for rule history;
- validate effective dates and overlaps;
- record lineage from rules to curated outputs;
- define recompute scope when a rule changes.

Deliverables:

- governed rule tables;
- rule history model;
- DQ rule catalog;
- lineage event structure;
- targeted replay metadata.

## Phase 4: Curated Model Rationalization

Goals:

- define curated fact, dimension, and bridge grains;
- remove redundant intermediate objects;
- separate audit fields from analysis-grade outputs;
- introduce approved adjustment pattern for legacy parity;
- publish stable curated outputs for priority reporting.

Deliverables:

- curated object inventory;
- semantic output definitions;
- reconciliation approach;
- retired or deferred object list;
- performance baseline for priority pipelines.

## Phase 5: Pipeline Decoupling and Reliability

Goals:

- break large procedural paths into observable responsibilities;
- isolate ingestion, standardization, rule application, DQ, and publication;
- design targeted replay for late files and rule changes;
- record row counts, exceptions, and publication status by run.

Deliverables:

- decoupled orchestration design;
- failure-boundary matrix;
- replay and backfill runbook;
- operational monitoring checklist;
- controlled cutover plan.

## Phase 6: Thin Semantic Serving

Goals:

- move repeated BI logic into curated or semantic outputs;
- publish clear metric definitions and aggregation rules;
- reduce report-side transformation logic;
- validate priority outputs through dual-run comparison.

Deliverables:

- semantic output catalog;
- metric definition notes;
- BI consumption contract;
- dual-run validation results;
- decommission candidate list.

## Phase 7: AI-Ready Operations

Goals:

- expose approved metadata for assistant retrieval;
- support DQ triage summaries;
- support lineage explanation;
- support schema drift explanation;
- support rerun planning drafts with human approval.

Deliverables:

- AI context policy;
- retrieval-ready metadata catalog;
- assistant use-case backlog;
- guardrail checklist;
- audit and approval workflow.

## Delivery Principle

Modernization should move in controlled slices: one source family, one rule family, one curated output, and one semantic surface at a time.

The target is not a dramatic rewrite. The target is steady replacement of opaque coupled behavior with explicit, governed, explainable platform responsibilities.
