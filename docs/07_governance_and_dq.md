# 07. Governance and DQ

Governance in this project is practical. It is not documentation for its own sake. It is the set of controls that lets the platform explain where data came from, what rule shaped it, and whether it is safe to publish.

## Source Contracts

Each major source should have a contract that defines:

- source owner;
- delivery cadence;
- expected file or extract pattern;
- required columns and types;
- business date interpretation;
- key candidates;
- duplicate handling;
- late-arrival behavior;
- schema drift policy;
- quarantine behavior;
- reconciliation expectation.

Without source contracts, downstream logic keeps rediscovering source behavior.

## Governed Rule History

Business rules should remain business-owned, but the warehouse should manage history and validation.

Target pattern:

```text
business editing surface
  -> current-state extract
  -> STG standardization
  -> row_hash comparison
  -> CTRL rule history
  -> CUR serving rules
```

Important behaviors:

- a real business content change creates a new history version;
- a touch-save without business change is a no-op;
- physical delete is discouraged in favor of inactive status;
- overlapping effective periods are blocked or quarantined;
- downstream facts recompute only affected dates, entities, or keys.

## DQ Rule Themes

Minimum DQ themes:

- required columns present;
- expected data types parse correctly;
- source file or batch is not duplicated;
- deterministic key is unique at expected grain;
- valid date windows;
- non-overlapping effective periods;
- successful mapping resolution;
- valid numeric ranges;
- source-to-curated reconciliation;
- no sensitive raw field exposure in curated outputs;
- traceable quarantine reason for rejected records.

## Exception Store

DQ exceptions should be stored as analytical data, not hidden in logs.

Each exception should identify:

- rule ID;
- severity;
- source contract;
- batch or file reference;
- impacted row, key, date, or rule;
- detected value;
- expected condition;
- owner or review queue;
- disposition status.

This gives engineers, analysts, data owners, and future AI assistants the same operating context.

## Lineage

Lineage should connect curated outputs back to:

- source records or batches;
- source contract version;
- schema version;
- rule rows;
- adjustment rows;
- DQ checks;
- publication run.

The goal is not to draw lineage diagrams for appearance. The goal is to answer why a number exists and what would need to rerun if its inputs changed.

## Governance Outcome

The platform becomes easier to operate because meaning is no longer hidden across procedures, files, and BI logic. It becomes safer to extend because source contracts, rule history, DQ exceptions, and lineage are explicit.
