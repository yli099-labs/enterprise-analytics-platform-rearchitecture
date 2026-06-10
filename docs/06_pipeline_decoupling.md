# 06. Pipeline Decoupling

The third major re-architecture move was to reduce the black-box procedure problem.

Large coupled procedures can be fast on a good day and painful on a bad day. When one part times out or behaves unexpectedly, the pipeline may show a failed step without showing the exact business or technical boundary that failed.

## Design Direction

The redesign decouples:

- ingestion from transformation;
- source-specific cleanup from cross-domain business logic;
- audit and archive loading from analytical serving;
- rule validation from rule application;
- curated publication from BI consumption;
- full reruns from targeted replay.

Reliability does not only come from faster code. It comes from smaller, explainable failure boundaries.

## Failure Boundary Model

Each pipeline step should have:

- one primary responsibility;
- declared inputs and outputs;
- clear validation checks;
- lineage event creation;
- retry or replay behavior;
- ownership for failures;
- promotion criteria before downstream publication.

## Example Decoupled Flow

```text
1. Receive source file into LANDING.
2. Register file and batch metadata.
3. Preserve source evidence in RAW.
4. Standardize types and keys in STG.
5. Validate source contract and DQ rules in CTRL.
6. Apply governed business rules.
7. Publish affected CUR objects.
8. Refresh thin SEM views.
9. Record lineage and reconciliation status.
```

If a failure occurs at step 5, the platform should show which contract, file, column, key, or rule failed. It should not require opening a large procedure and reconstructing the path manually.

## Targeted Replay

Targeted replay depends on metadata.

The platform needs to know:

- which source batch arrived;
- which dates, entities, or keys are affected;
- which rule versions were active;
- which curated objects depend on those inputs;
- which downstream semantic outputs require refresh;
- which validations must pass before publication.

This is the difference between rerunning a whole estate and recomputing an impacted slice.

## Observability

Minimum observability signals include:

- batch ID;
- source contract version;
- schema version;
- row count by layer;
- accepted, rejected, and quarantined count;
- DQ rule outcomes;
- rule version applied;
- curated object refreshed;
- lineage event ID;
- publication status.

## Result

Pipeline decoupling improves operations because failures become diagnosable events. It also supports AI readiness because future assistants can read structured run, lineage, and DQ metadata instead of guessing from logs.
