# DQ Rule Catalog

This catalog shows public-safe examples of data quality rules for the target platform.

| Rule ID | Layer | Rule theme | Example condition | Failure owner |
| --- | --- | --- | --- | --- |
| `DQ_SRC_001` | `LANDING` | Required file metadata | Batch ID, source label, and received timestamp are populated. | Platform owner |
| `DQ_SRC_002` | `RAW` | Duplicate batch | File or batch hash has not been accepted before. | Platform owner |
| `DQ_STG_001` | `STG` | Required columns | Contract-required fields exist and are parseable. | Source owner |
| `DQ_STG_002` | `STG` | Business date | Business date maps to a valid reporting period. | Source owner |
| `DQ_STG_003` | `STG` | Deterministic key | Natural key fields generate a non-null hash key. | Platform owner |
| `DQ_CTRL_001` | `CTRL` | Rule history | Effective date ranges do not overlap for the same business key. | Business owner |
| `DQ_CTRL_002` | `CTRL` | Mapping resolution | Required business mapping resolves to one active rule row. | Business owner |
| `DQ_CUR_001` | `CUR` | Grain uniqueness | Curated fact is unique at declared grain. | Data owner |
| `DQ_CUR_002` | `CUR` | Measure validity | Published measure values stay within allowed range. | Data owner |
| `DQ_SEM_001` | `SEM` | Semantic readiness | Measures and dimensions match approved semantic definition. | Analytics owner |
| `DQ_PRIV_001` | `CUR` | Privacy boundary | Restricted raw fields are excluded or masked before curated publication. | Platform owner |

## Exception Record Shape

Each failed rule should produce an exception record with:

- rule ID;
- severity;
- layer;
- source contract;
- file or batch ID;
- impacted business date;
- impacted key or rule row;
- expected condition;
- detected value;
- owner group;
- disposition status;
- lineage event ID.
