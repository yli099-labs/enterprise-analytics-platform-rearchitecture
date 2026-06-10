# 01. Problem Statement

The legacy warehouse was still useful. It produced recurring reports and contained years of business logic. The problem was that it had become brittle: ingestion, historical retention, transformations, business rules, audit evidence, orchestration, and BI semantics were too tightly coupled.

This was not a simple SQL tuning problem. Performance issues were visible, but they were symptoms of deeper architecture debt.

## Core Problem

The warehouse was doing too many jobs at once.

| Function | Legacy problem |
| --- | --- |
| Ingestion | Source behavior was learned through pipeline behavior rather than explicit contracts. |
| Historical retention | Old data was repeatedly touched by nightly processing. |
| Transformation | ETL and business logic were buried inside large procedural steps. |
| Business rules | Rules lived across SQL, files, and BI models. |
| Audit | Audit-only data was mixed with analysis-grade serving data. |
| BI serving | Reports depended on hidden or repeated logic. |
| Operations | Failures were hard to localize because steps were too coupled. |
| AI readiness | Metadata and lineage were not explicit enough for safe agent use. |

The redesign needed to create clear architectural boundaries.

## Why This Was Dangerous

A slow system is frustrating. An opaque system is risky.

When responsibilities are coupled:

- a small source change can break downstream reporting;
- reruns are risky because the impacted slice is unclear;
- analysts cannot easily explain why a number changed;
- manual workarounds can become permanent hidden logic;
- low-value data can consume the same nightly compute as core analytical data;
- AI or agentic workflows cannot reason safely because contracts, lineage, and rule boundaries are not explicit.

## Design Principle

Every curated number should be explainable back to a source record, source file, schema version, business-rule row, or approved adjustment.

This principle forces the architecture to answer:

- Where did this data come from?
- What business rule shaped it?
- What grain is the curated output?
- Which historical period is active?
- What is analytical data versus audit evidence?
- What should run nightly versus periodically?
- What can be safely exposed to BI or future AI assistants?

## Success Criteria

The redesign is successful if it creates:

- a clear `LANDING -> RAW -> STG -> CTRL -> CUR -> SEM` operating model;
- lifecycle-aware processing that avoids unnecessary historical scans;
- governed curated facts, dimensions, bridges, and semantic outputs;
- source contracts and schema registries for major inputs;
- rule history and validation for business-owned mappings;
- DQ exceptions with traceable source, batch, key, or rule context;
- smaller failure boundaries and targeted replay behavior;
- enough metadata for AI-assisted documentation, DQ triage, lineage explanation, and rerun planning.

## Non-Goals

This case study does not claim to:

- expose real production code or schemas;
- rebuild every legacy report;
- solve real-time streaming requirements;
- put AI on top of raw private data;
- replace human ownership of business meaning.

The scope is platform modernization beyond tool replacement.
