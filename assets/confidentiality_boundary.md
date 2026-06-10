# Confidentiality Boundary

This repository is designed for public review and portfolio use.

## Not Included

The repo intentionally excludes:

- real organization, team, employee, vendor, platform, source system, report, table, network path, file, or endpoint names;
- production credentials, tokens, hostnames, tenant IDs, subscription IDs, storage paths, connection strings, or access keys;
- exact production schemas, row counts, business KPI values, exception volumes, or private data definitions;
- copied production SQL, orchestration code, BI model files, or operational runbooks;
- raw or sampled production records.

## Public-Safe Substitutions

Use logical labels instead:

| Private detail type | Public-safe replacement |
| --- | --- |
| Organization name | `Organization A` |
| Source system name | `Source A`, `Source B`, `Source C` |
| Table name | `RAW_SOURCE_A`, `CUR_FACT_X`, `SEM_VIEW_Y` |
| Rule file name | `RULE_SET_B` |
| Report name | `Priority Reporting Surface` |
| Exact volume | `multi-year history`, `multi-hour runtime`, `shorter controlled window` |
| Exact KPI | `priority metric`, `curated measure`, `reporting output` |

## Writing Rule

Describe the architecture pattern, decision logic, and operating control. Do not describe private implementation details that would identify a real organization, system, dataset, or person.
