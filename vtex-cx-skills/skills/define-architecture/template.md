# Architecture Document: [FEATURE NAME]

**Feature**: `[###-feature-name]`

**Verdict**: [full | contract-only | not-required]

**Status**: [Draft | Approved | Not required | Superseded by <link>]

**Version**: [arch-vN] — tag `[###-feature-name]/arch-vN` once approved

**Created**: [DATE] | **Last amended**: [DATE]

<!--
  This is an ARCHITECTURE DOCUMENT, not a spec. It decides what crosses a
  boundary between repositories, teams or services: contracts, data
  ownership, consistency, binding non-functional requirements and delivery
  sequence. Anything a single repository can change without anyone outside it
  noticing belongs to that repository's Engineering Spec, not here.

  It MUST NOT restate or redefine the Product Spec: problem, scope, journeys
  and success criteria are inherited.

  Sections by verdict:
  - not-required: Inheritance, Assessment.
  - contract-only: Inheritance, Assessment, Approval, Impact Map, Contracts,
    Delivery Sequence, Risks, Amendment Log.
  - full: every section.
  Remove the sections the verdict does not require. Never leave "N/A".
-->

## Inheritance from Product Spec

- Product Spec: [title] — [permalink]
- Pinned version: [commit/tag]
- Inherited binding decisions: [BD-IDs that constrain this design]
- Divergences: [none | link to amendment in the Product Spec]

## Assessment

| Criterion | Applies | Evidence in the Product Spec |
|-----------|---------|------------------------------|
| More than one repository or team changes | [yes/no] | [section or ID] |
| A public interface between repositories changes | [yes/no] | [section or ID] |
| New service, datastore, queue or infrastructure | [yes/no] | [section or ID] |
| Data owned by one service is written or read by another | [yes/no] | [section or ID] |
| Security, privacy or compliance impact | [yes/no] | [section or ID] |
| Scale beyond what the affected services handle today | [yes/no] | [section or ID] |

**Verdict**: [full | contract-only | not-required] — [one-paragraph rationale]

## Approval

- Technical reference (author): [name]

| Repository | Tech lead | Status |
|------------|-----------|--------|
| [repo] | [name] | [pending / approved] |

## Impact Map

<!--
  Defines the slicing: the "Scope of this spec" of each Engineering Spec is
  derived from this table.
-->

| Repository / service | Domain | Role in this feature | Engineering Spec expected | Constitution version |
|----------------------|--------|----------------------|---------------------------|----------------------|
| [engineering/repo] | [backend / frontend / frontend-platform / cloud] | [what it delivers] | [yes / no] | [x.y.z or missing] |

**External dependencies**: [other products or teams outside the submodules, with a named owner, or "None"]

## Solution Overview

### Components

```mermaid
flowchart LR
  %% container-level view: repositories, services, datastores, queues
```

### Main Flows

<!-- One sequence per main flow, including at least one failure path. -->

```mermaid
sequenceDiagram
```

## Decisions

<!--
  Only decisions that cross a boundary. "binding" decisions are inherited by
  every Engineering Spec in the Impact Map; "guidance" is a recommendation.
  Only the technical reference promotes a decision to binding.
-->

### AD-001 — [title] `[binding | guidance]`

- **Context**: [what forces the decision, with references to BD/NFR/FR IDs]
- **Decision**: [what was chosen]
- **Alternatives considered**: [option — why it was rejected]
- **Consequences**: [what becomes easier, what becomes more expensive]
- **Constitution constraints honored**: [repo — principle — how]
- **Decided by**: [name, date]

## Contracts

<!--
  Machine-readable files under ./contracts/ are the source of truth. This
  table is their complete index, with paths relative to this document: every
  file has a row and every row's file exists. Engineering Specs discover the
  contracts through this table. The prose below does not redefine them.
-->

| Contract | Kind | Producer | Consumers | File | Version | Backward compatible |
|----------|------|----------|-----------|------|---------|---------------------|
| [name] | [HTTP / event / host message] | [repo] | [repos] | [contracts/...] | [x.y.z] | [yes / no + deprecation path] |

### Cross-Cutting Conventions

- **Error model**: [shape of the error body, codes, what the client sees when authorization fails]
- **Authentication and authorization**: [where identity comes from, which check is server-side]
- **Pagination and filtering**: [convention, or "not applicable to this feature"]
- **Idempotency**: [which operations, which key, retention of the key]
- **Naming and casing**: [the producer's convention; consumers adapt at their boundary]
- **Correlation ID**: [header name, who generates it, how it crosses services]

### Compatibility and Deprecation

[How these contracts evolve, how breaking changes are announced, and the compatibility window during rollout.]

## Data

| Entity | Owner service | Datastore | Readers / writers outside the owner | Consistency |
|--------|---------------|-----------|-------------------------------------|-------------|
| [entity] | [repo] | [store] | [repo — read/write — via which contract] | [sync / eventual / saga] |

**Personal data, retention and compliance**: [classification, retention, legal basis, derived from Privacy & Data Protection]

## Binding Non-Functional Requirements

<!-- Each Engineering Spec derives the peak of its own service from this table. -->

| Flow | Peak (with window) | Latency target | Error budget | Derived from |
|------|--------------------|----------------|--------------|--------------|
| [flow] | [value, unit, window] | [p95/p99] | [value] | [NFR ID] |

## Delivery Sequence and Parallelism

- **In parallel against the contract mocks**: [what each repo can build from day one]
- **Must ship first**: [what, and behind which flag]
- **Deploy order and compatibility window**: [order across repositories, flags, how long old and new versions coexist]
- **Rollback**: [what can be rolled back independently, and what cannot]

## Risks and Open Questions

- [risk or question] — Owner: [name] — Blocks: [what, or "nothing"]

## Amendment Log

| Version (tag) | Change | Reason | Approved by | Specs that must re-pin |
|---------------|--------|--------|-------------|------------------------|
| arch-v1 | Initial version | — | [names] | — |
