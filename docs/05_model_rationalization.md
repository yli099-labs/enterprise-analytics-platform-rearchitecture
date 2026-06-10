# 05. Model Rationalization

The second major re-architecture move was to simplify the model and move repeated business meaning into governed layers.

The goal was not minimalism for appearance. The goal was operational clarity.

## Legacy Model Issues

The legacy estate contained:

- redundant tables and views;
- procedure outputs that existed only for narrow report shapes;
- transformations duplicated across SQL and BI;
- unclear fact and dimension grain;
- audit fields mixed into analysis-grade outputs;
- business rules embedded in code paths that were hard to review.

These objects were not all equally meaningful. Some were core analytical structures. Some were historical leftovers. Some existed because a prior report needed a specific shape.

## Rationalization Approach

The redesign rationalized the target model by:

- declaring the grain of each curated fact;
- separating facts, dimensions, bridges, rules, and audit evidence;
- reducing redundant intermediate objects;
- moving repeated business logic into governed transformation layers;
- narrowing curated outputs to analysis-grade fields;
- keeping raw evidence wide for audit and replay;
- exposing stable semantic outputs to BI.

## Curated Object Standards

Every curated object should define:

- purpose;
- grain;
- primary business keys;
- source contribution;
- applied rule sets;
- lifecycle treatment;
- DQ expectations;
- sensitive-field policy;
- downstream semantic outputs.

This makes the model easier to test, explain, and extend.

## Thin BI Consumption

BI should consume curated semantic outputs rather than become the hidden transformation layer.

The semantic layer may provide:

- user-facing names;
- metric descriptions;
- aggregation-safe measures;
- common filters;
- access-controlled views;
- report-friendly joins.

It should not reimplement source parsing, effective-dated mapping, schema resolution, business-hour expansion, reconciliation adjustments, or core KPI logic.

## Legacy Parity Pattern

When approved historical results must reconcile to prior reporting, the base curated fact should remain clean.

Recommended pattern:

```text
base_curated_fact
UNION ALL
approved_adjustment_fact
= final_reporting_fact
```

Adjustment rows store governance metadata, approval status, reason code, and effective period. This gives consumers one final reporting object while preserving auditability.

## Result

Model rationalization reduces ambiguity. Users and engineers can understand what each object means, why it exists, what grain it represents, and what downstream semantic output it supports.
