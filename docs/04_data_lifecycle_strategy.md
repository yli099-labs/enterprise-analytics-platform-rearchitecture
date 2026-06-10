# 04. Data Lifecycle Strategy

The first major re-architecture move was to stop treating all historical data as if it needed to be processed every night.

Runtime improvement came from changing the work the platform performed, not only making the same work faster.

## Core Idea

You do not optimize a pipeline by making it run faster over unnecessary data. You optimize it first by making it stop touching unnecessary data.

## Lifecycle Categories

| Category | Treatment |
| --- | --- |
| Hot analytical window | Refreshed through the governed nightly path. |
| Warm correction window | Eligible for targeted recompute when late files, corrections, or rule changes arrive. |
| Cold historical archive | Retained for audit, lineage, and controlled backfill, but not scanned nightly by default. |
| Audit-only data | Preserved or periodically refreshed without heavy daily compute. |
| Low-quality or unstable source | Quarantined, redesigned, or deferred until quality improves. |
| Reference or rule data | Governed with history, validation, ownership, and effective dates. |

## Source Prioritization

Not every source deserves equal treatment.

The redesign classifies inputs by analytical value and operational behavior:

- core sources that feed recurring analytical outputs;
- sources needed for audit or traceability;
- unstable feeds that require quality work before curated modeling;
- low-value feeds that should not slow the nightly path;
- business-owned rules that require validation and history.

This prevents the platform from becoming a place where every available file is transformed nightly simply because it exists.

## Processing Patterns

| Pattern | Use when |
| --- | --- |
| Append | The source represents immutable events or records. |
| Partition replace | A source restates a complete business date, period, or partition. |
| Merge | The source sends corrections to existing records. |
| SCD2 history | Business meaning changes over time and must preserve historical interpretation. |
| Archive only | Data is needed for audit or future analysis but not daily curated serving. |
| Targeted recompute | A late file or rule change affects a known slice of dates, entities, or keys. |

The platform should choose the pattern by source behavior, not by one default loading habit.

## Recompute Scope

The key operating question is:

What exactly needs to rerun?

For each batch or rule change, the control layer should record:

- impacted source file or batch;
- impacted business date or period;
- impacted business key or entity;
- impacted rule set;
- impacted curated object;
- required validation and reconciliation status.

This supports targeted replay instead of broad reruns.

## Historical Retention

Historical data remains available, but it is separated from daily analytical compute.

The platform keeps:

- raw evidence for audit and replay;
- historical curated output for comparison and reporting;
- approved adjustments where legacy parity is required;
- lineage events that explain how historical values were produced;
- lifecycle policy that defines when a period is active, closed, frozen, or archive-only.

## Outcome

Lifecycle-aware processing improves runtime because the platform stops doing unnecessary daily work. It improves reliability because older stable data is not repeatedly exposed to the same nightly failure path. It improves explainability because every recompute has a defined scope and reason.
