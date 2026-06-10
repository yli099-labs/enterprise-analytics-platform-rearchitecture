# 02. Legacy Estate Diagnosis

The legacy estate had working pipelines, but the operating model had drifted into a coupled reporting system. The visible pain was runtime and reliability. The deeper issue was unclear responsibility boundaries.

## Starting Point

The legacy state contained:

- file-based source feeds;
- cloud-style orchestration;
- a SQL-based warehouse;
- large procedural transformation steps;
- staging tables rebuilt through broad reload patterns;
- BI reports depending on hidden warehouse and report-side logic;
- historical data retained inside operational processing paths;
- audit and analytical serving data mixed together.

## Visible Symptoms

Common symptoms included:

- long nightly runtime, sometimes around several hours;
- recurring timeout or stuck-step failures;
- broad scans over years of historical data;
- redundant transformations across procedures, views, and reports;
- unclear model relationships;
- difficult root-cause analysis;
- unclear boundary between analysis-grade data and audit-only data.

## Root Causes

### 1. Historical Data Was Treated as Daily Work

Stable historical periods were repeatedly scanned or transformed as part of the nightly path. This created compute waste and increased the chance that an unrelated older period could affect current processing.

### 2. Procedural Logic Became the System Boundary

Large procedures combined source cleanup, transformation, rule application, audit behavior, and reporting preparation. When something failed, the pipeline could identify the procedure but not always the business responsibility that failed inside it.

### 3. BI Was Carrying Too Much Meaning

BI models and reports contained logic that should have been resolved upstream. This made reporting fast to patch but difficult to govern, test, and reconcile.

### 4. Sources Were Loaded Because They Existed

Not every data source deserves the same nightly treatment. Some sources support core analytics. Others are audit-only, low-quality, unstable, or useful only for future investigation. Treating them equally made the platform heavier and less explainable.

### 5. Metadata Was Not AI-Readable

The estate had knowledge, but much of it lived in people, procedures, file naming conventions, or report behavior. That is not enough for safe AI-assisted operations. Future assistants need explicit contracts, lineage, DQ results, rule history, and curated semantic definitions.

## Failure Modes

| Failure mode | Old pattern | Design response |
| --- | --- | --- |
| Compute waste | Nightly jobs repeatedly touched long historical windows. | Lifecycle-aware hot/cold separation and targeted recompute. |
| Logic opacity | Business rules were scattered across procedures, files, and BI. | Governed rule history, declared grains, and curated semantic outputs. |
| Operational fragility | Large coupled steps caused unclear failures and broad reruns. | Smaller observable steps, lineage metadata, and replay scoping. |

## Diagnosis Summary

The platform did not need only faster SQL. It needed a new operating model.

The redesign separated source evidence, operational processing, business meaning, and consumption layers so the system could become faster, more reliable, explainable, and AI-ready.
