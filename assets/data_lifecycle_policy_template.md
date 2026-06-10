# Data Lifecycle Policy Template

Use this template to decide how a source or curated object should be processed over time.

## Object Overview

| Field | Value |
| --- | --- |
| Object label | `CUR_FACT_X` |
| Object type | Source, raw table, staged table, curated fact, curated dimension, semantic view |
| Business owner | Owner group |
| Technical owner | Owner group |
| Primary grain | One row per ... |
| Refresh cadence | Daily, periodic, archive-only, on demand |

## Lifecycle Zones

| Zone | Definition | Processing behavior |
| --- | --- | --- |
| Hot | Active analytical window | Nightly governed refresh |
| Warm | Recent correction window | Targeted recompute when impacted |
| Cold | Stable historical window | Retained, not scanned nightly by default |
| Archive | Audit or backfill evidence | Preserved with minimal transformation |

## Recompute Triggers

| Trigger | Impact scope |
| --- | --- |
| Late source file | Business dates or keys from source contract |
| Rule change | Effective date and impacted entities |
| Schema version change | Affected source batches and dependent curated objects |
| DQ correction | Failed rule scope |
| Approved adjustment | Reporting output and reconciliation period |

## Retention and Access

- Raw evidence retention: TBD.
- Curated retention: TBD.
- Semantic output retention: TBD.
- Sensitive fields restricted to: TBD.
- Archive access approval path: TBD.

## Publication Criteria

- Source contract validated.
- Required DQ checks passed or approved exceptions recorded.
- Recompute scope documented.
- Lineage events written.
- Semantic definitions reviewed.
