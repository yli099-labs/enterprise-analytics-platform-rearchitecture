# Semantic Output Template

Use this template to define a BI or semantic-serving output over curated data.

## Output Overview

| Field | Value |
| --- | --- |
| Output name | `SEM_VIEW_Y` |
| Curated dependency | `CUR_FACT_X`, `CUR_DIM_Z` |
| Business purpose | Explain the decision or analysis supported |
| Owner | Business or analytics owner group |
| Refresh cadence | Daily, weekly, monthly, or on demand |

## Grain

Declare the row grain in one sentence.

Example:

```text
One row per business date, business entity, and approved metric.
```

## Measures

| Measure | Definition | Aggregation rule | Source or rule dependency |
| --- | --- | --- | --- |
| `metric_a` | Public-safe definition | Sum, count, average, last value, non-additive | `CUR_FACT_X`, `RULE_SET_B` |

## Dimensions

| Dimension | Definition | Source or rule dependency |
| --- | --- | --- |
| `business_date` | Reporting date used for analysis | Source contract |
| `entity_group` | Governed grouping used for reporting | Rule history |

## Access Boundary

- No private raw identifiers should appear in the semantic output.
- Sensitive source fields should be masked, hashed, aggregated, or excluded.
- The output should expose only analysis-grade fields.

## Validation

- Grain uniqueness passes.
- Measures reconcile to curated source objects.
- Required dimensions are populated.
- DQ exceptions are reviewed before publication.
- Metric definitions match approved semantic wording.
