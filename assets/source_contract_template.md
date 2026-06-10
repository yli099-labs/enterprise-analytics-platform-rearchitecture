# Source Contract Template

Use this template to document a source before it enters the governed analytical path.

## Source Overview

| Field | Value |
| --- | --- |
| Source label | `Source A` |
| Source owner | Business or data owner group |
| Technical owner | Platform owner group |
| Delivery cadence | Daily, weekly, ad hoc, or periodic |
| Source pattern | Full extract, delta, snapshot, append-only event, manual rule input |
| Analytical priority | Core, audit-only, deferred, quarantine |

## Expected Structure

| Field | Description |
| --- | --- |
| Required columns | Columns that must exist for load acceptance |
| Optional columns | Columns accepted but not required |
| Business date | Field or rule used to assign reporting date |
| Timezone | Expected timezone or normalization rule |
| Key candidates | Candidate fields for deterministic key creation |
| Schema drift policy | Reject, quarantine, register new schema, or allow compatible additions |

## Load Behavior

| Question | Answer |
| --- | --- |
| Is the source append-only? | TBD |
| Can the same business date be restated? | TBD |
| Can late data arrive? | TBD |
| What is the duplicate rule? | TBD |
| What is the replay strategy? | Append, partition replace, merge, SCD2, or archive-only |

## DQ Requirements

- Required columns are present.
- Business date parses successfully.
- Deterministic key is populated.
- Duplicates are handled according to contract.
- Counts reconcile within expected tolerance.
- Sensitive fields remain restricted to approved layers.

## Lineage Requirements

Each accepted batch should record:

- source label;
- contract version;
- file or batch ID;
- schema version;
- load timestamp;
- accepted row count;
- rejected or quarantined row count;
- impacted curated objects;
- publication status.
