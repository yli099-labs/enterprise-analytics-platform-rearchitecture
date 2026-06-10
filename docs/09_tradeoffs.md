# 09. Trade-Offs

This redesign is pragmatic. The goal is not theoretical purity. The goal is a platform that a real team can operate, explain, rerun, extend, and safely connect to AI-assisted workflows.

## 1. Architecture Redesign vs Direct Migration

**Decision:** Use a layered operating model instead of directly moving old procedures into a new platform.

**Why:** A direct migration would preserve the coupling between ingestion, staging, transformation, business rules, and BI.

**Trade-off:** More upfront design work, but clearer ownership, replay behavior, and long-term maintainability.

## 2. Lifecycle-Aware Processing vs Broad Nightly Reload

**Decision:** Separate hot analytical refresh, warm correction windows, and cold history.

**Why:** Stable history does not need to consume the same nightly compute as active data.

**Trade-off:** Lifecycle policy must be designed and maintained, but runtime improvement becomes structural.

## 3. Curated Truth vs Report-Side Logic

**Decision:** Resolve core business logic in governed curated outputs.

**Why:** Report-side logic is quick to patch but hard to govern, test, and reconcile.

**Trade-off:** Curated transformations need more discipline, but BI becomes thinner and more consistent.

## 4. Rule History vs Manual Current-State Files

**Decision:** Keep business-friendly editing, but move history and validation into the warehouse.

**Why:** Users should maintain business meaning, not warehouse version mechanics.

**Trade-off:** The platform must detect real content changes and validate effective dates.

## 5. Source Prioritization vs Load Everything

**Decision:** Treat source feeds differently based on analytical value and quality.

**Why:** Audit-only or unstable data should not slow the nightly analytical path by default.

**Trade-off:** Some feeds remain archive-only or deferred until a clear requirement promotes them.

## 6. Smaller Failure Boundaries vs One Large Procedure

**Decision:** Break procedural logic into observable responsibilities.

**Why:** A smaller step is easier to validate, retry, explain, and assign ownership to.

**Trade-off:** More orchestration design is required, but failures become diagnosable.

## 7. Raw Evidence Wide vs Curated Outputs Narrow

**Decision:** Preserve source evidence in controlled layers while publishing narrow analysis-grade outputs.

**Why:** Wide raw storage supports audit and replay. Narrow curated outputs reduce clutter and privacy risk.

**Trade-off:** Some future analysis may need to return to raw or staged layers.

## 8. AI Assistance After Data Controls

**Decision:** Build AI use cases on metadata, contracts, DQ results, lineage, and semantic definitions.

**Why:** AI cannot safely reason over ambiguous business meaning or missing lineage.

**Trade-off:** AI features arrive after the foundation is explicit, not before.

## Known Risks and Controls

| Risk | Control |
| --- | --- |
| Source schema changes silently | Source contracts, file registry, schema registry. |
| Duplicate loads | Deterministic keys and batch registry. |
| Manual rule edits break KPIs | Rule history, validation, exception reports. |
| Historical changes rewrite meaning | Effective-dated rules and approved adjustments. |
| BI logic diverges | Thin BI over curated semantic outputs. |
| Legacy parity pressure pollutes facts | Separate approved adjustment facts. |
| Sensitive fields leak | Raw-layer restrictions and curated minimization. |
| AI gives unsupported answers | Retrieval from approved metadata with citation requirements. |

## Practical Conclusion

The main trade-off is speed versus trust.

The selected design is not the fastest way to load files into tables. It is the faster path to a platform that can be maintained, explained, reconciled, and safely extended into AI-assisted operations.
