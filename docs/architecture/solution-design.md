# Solution Design — EuroHealth AI Helpdesk
## Architecture Blueprint (Co-Design Phase Deliverable)

**Version:** 0.1 DRAFT
**Date:** 2026-02-25
**Primary Authors:** FDE, AI-SE
**Contributors:** All roles
**Status:** Under development (Day 13)

**Prerequisite:** [Consolidated Discovery Report](../discovery/consolidated-discovery-report.md)

---

## 1. System Overview

### 1.1 What We Are Building

<!-- FDE: 2-3 sentences. What is the system, who uses it, what does it do? -->

### 1.2 Design Principles

<!-- Derived from discovery findings. Examples: -->
<!-- - Governance-first: every AI response passes through policy enforcement -->
<!-- - On-prem only: no data leaves EuroHealth infrastructure -->
<!-- - Auditability: every decision is logged and reconstructable -->
<!-- - Incremental: Phase 1 handles L1 tickets only -->

### 1.3 Out of Scope (Phase 1)

<!-- Explicitly list what we are NOT building. This prevents scope creep. -->

---

## 2. Architecture Overview

### 2.1 High-Level Pipeline

```
┌─────────┐    ┌───────────┐    ┌───────────┐    ┌─────────┐    ┌──────────┐
│  User    │───▶│ Retriever │───▶│ Generator │───▶│   PEP   │───▶│ Response │
│  Query   │    │ (RAG)     │    │ (LLM)     │    │ (Policy │    │          │
└─────────┘    └───────────┘    └───────────┘    │  Check) │    └──────────┘
                    │                               │    ▲         │
                    ▼                               │    │         ▼
              ┌───────────┐                    ┌────┴────┐   ┌──────────┐
              │ Vector DB │                    │   PDP   │   │  Audit   │
              │ (Confluence│                   │ (Policy │   │   Log    │
              │  2000 docs)│                   │  Rules) │   │          │
              └───────────┘                    └─────────┘   └──────────┘
                                                    ▲
                                                    │
                                              ┌─────────┐
                                              │ YAML    │
                                              │ Policies│
                                              └─────────┘
```

### 2.2 Component List

| Component | Owner | Technology | Status |
|-----------|-------|-----------|--------|
| User Interface | AI-FE | <!-- web app, Teams integration, etc. --> | Design |
| API Gateway | FDE | <!-- --> | Design |
| Retriever (RAG) | FDE | <!-- vector DB, embedding model --> | Design |
| Generator (LLM) | FDE + AI-SE | <!-- on-prem LLM selection --> | Pending infra validation |
| Policy Engine (PDP) | AI-SEC + AI-SE | YAML rules + Python evaluator | Design |
| Policy Enforcement (PEP) | FDE + AI-SEC | Pipeline middleware | Design |
| Audit Logger | AI-SE | <!-- structured logging --> | Design |
| Monitoring Dashboard | AI-DA | <!-- Grafana, custom, etc. --> | Design |
| Golden Dataset | AI-DS | JSON question/answer pairs | Design |
| ServiceNow Integration | AI-SE | <!-- REST API --> | Pending API validation |

---

## 3. Component Specifications

### 3.1 Retriever (RAG Pipeline) — FDE

<!-- 
FDE: Describe the retrieval system.
- Source: 2,000 Confluence pages (EN/DE/CZ)
- Chunking strategy: how do you split documents?
- Embedding model: which one, why? (must run on-prem)
- Vector store: which one, why?
- Top-K retrieval: how many chunks per query?
- Relevance threshold: minimum confidence score?
-->

### 3.2 Generator (LLM) — FDE + AI-SE

Phase 1 generator baseline is an on-prem instruction-tuned 8B class model exposed through an internal inference service. The selection criteria are deterministic behavior, multilingual quality in EN/DE/CZ, and acceptable latency under 12 concurrent helpdesk agents.

- Model profile: 8B instruction model, fixed production tag (for example `llama-3.2-8b-v1`)
- Runtime: containerized inference service with internal-only API
- Target serving shape: 1 production GPU node + 1 warm standby node
- Capacity assumption: 12 concurrent agents, p95 generation latency under 1500ms for standard L1 queries
- Context budget: 8k working context with retrieval chunks capped by token budget
- Sampling defaults: temperature `0.2`, top_p `0.9`, max_tokens `500`
- Prompt strategy: stable, versioned system prompt in Git; prompt changes follow the same approval and rollout gates as policy changes
- Language handling: preserve user language from request metadata (`en`, `de`, `cz`); no cross-language translation in Phase 1 unless no in-language context is available

Infrastructure validation (GPU model, VRAM headroom, throughput benchmark) is a Week 1 gate before model selection is marked final.

### 3.3 Policy Engine (PDP/PEP) — AI-SEC + FDE

<!--
AI-SEC: Describe the governance enforcement layer.
- PDP: How are policy rules evaluated?
- PEP: Where exactly in the pipeline does enforcement happen?
- Policy format: YAML structure and rule types
- Actions: block, redirect, escalate, redact, allow
- Fallback behavior: what happens if PDP is unreachable?
- Refer to: governance/policies/*.yaml
-->

### 3.4 Audit & Logging — AI-SE

Audit logging is mandatory for every policy decision path and is treated as compliance infrastructure, not optional observability.

What gets logged:
- Every PEP decision event (`allow`, `block`, `redirect`, `escalate`, `redact`)
- Every human override event from agent UI
- Every escalation routing event
- Every pipeline/system error event that affects decision integrity

Log format:
- Structured JSON aligned to `governance/evidence/audit-log-schema.json`
- Correlation keys: `session_id`, `query_hash`, `timestamp`, `model_version`
- Latency envelope captured as `latency_ms.retrieval`, `latency_ms.generation`, `latency_ms.policy_evaluation`, `latency_ms.total`

Retention and storage:
- PEP decision logs: 3 years minimum
- Query logs: 90 days, with anonymization after 30 days
- Override logs: 1 year
- Storage location: on-prem encrypted object storage bucket (`audit-logs`) with daily immutable snapshots and restricted RBAC (AI-SE + AI-SEC + compliance auditor roles)

Reconstruction procedure (Article 12 evidence):
1. Locate event window by `timestamp` and `session_id`.
2. Retrieve all related events by `query_hash` across `pep_decision`, `human_override`, `escalation`, `system_error`.
3. Rebuild decision timeline including policies and rule IDs evaluated.
4. Produce signed incident/reconstruction bundle (JSON export + checksum) within 24 hours of request.

Control requirements:
- Logging path is fail-safe: if audit write fails, raise P1 and stop normal response path until logging health is restored.
- Audit log completeness monitor alerts if no entries are written for >5 minutes.

### 3.5 Monitoring & Metrics — AI-DA

<!--
- KPI definitions: auto-resolve rate, escalation accuracy, override rate, etc.
- Collection points: where in the pipeline are metrics captured?
- Dashboard views: operational vs. board-level
- Alerting: when does a human get paged?
- Refer to: monitoring/dashboard-spec.md
-->

### 3.6 Evaluation Framework — AI-DS

<!--
- Golden dataset: size, coverage, language split
- Evaluation metrics: accuracy, precision, recall, F1
- Bias testing: cross-language performance comparison
- Drift detection: how to identify degradation over time
- Refer to: tests/golden_dataset/
-->

### 3.7 User Interface — AI-FE

<!--
- Interface type: web app / Teams integration / both
- Streaming: real-time response display
- Confidence indicators: how does the user see trust?
- HITL controls: override button, escalation trigger
- Policy block UX: what does the user see when PEP blocks?
- Accessibility: WCAG requirements
- Refer to: governance/operating-model/human-override-protocol.md
-->

---

## 4. Interface Contracts

> Detailed contracts in [interface-contracts.md](interface-contracts.md)

Summary of cross-component interfaces:

| From | To | Data | Format | Protocol |
|------|----|------|--------|----------|
| UI | API Gateway | User query + session | JSON | REST/WebSocket |
| API Gateway | Retriever | Query text + language | JSON | Internal |
| Retriever | Generator | Query + retrieved chunks | JSON | Internal |
| Generator | PEP | Draft response + metadata | JSON | Internal |
| PEP | PDP | Response + policy context | JSON | Internal |
| PDP | PEP | Decision (allow/block/redirect) | JSON | Internal |
| PEP | Audit Logger | Decision record | JSON | Async |
| PEP | UI | Final response OR block message | JSON | REST/WebSocket |
| All components | Monitoring | Metrics + traces | <!-- --> | <!-- --> |

---

## 5. Deployment Model — AI-SE

### 5.1 On-Premises Topology

Phase 1 deployment uses a segmented on-prem topology with strict east-west controls.

- Orchestration: Docker Compose for Phase 0/1 delivery speed; Kubernetes considered for Phase 2 scale-out
- Network zones:
  - `zone-ui`: Teams/web adapter and API gateway
  - `zone-ai`: retriever, generator, PDP/PEP services
  - `zone-data`: vector DB, audit storage, metrics store
- Allowed service paths:
  - UI/API Gateway -> Retriever/Generator/PEP
  - PEP -> Audit Logger (async append)
  - All services -> Monitoring collector
  - No direct UI access to storage backends
- Storage design:
  - Vector DB on encrypted on-prem volume with scheduled snapshot
  - Audit logs in encrypted object storage (`audit-logs`) + immutable daily snapshot
  - Metrics/time-series in monitoring storage with 13-month retention for trend reporting
- Scale target:
  - 12 concurrent helpdesk agents, baseline 20 active sessions alert threshold
  - Horizontal scale at API gateway and retriever; generator scales by GPU capacity
  - Degradation mode: prioritize low-latency allow/block path, escalate overflow queries to human queue

### 5.2 CI/CD Pipeline

CI/CD enforces governance checks as release gates.

Pipeline stages:
1. Commit + PR validation
- Markdown/YAML/JSON lint
- Policy schema validation for `governance/policies/*.yaml`
- Audit schema validation for `governance/evidence/audit-log-schema.json`
2. Test gates
- Unit tests (policy engine, logging, contract serialization)
- Integration tests (retriever -> generator -> PEP -> audit logger)
- Golden dataset evaluation gate (AI-DS owned thresholds)
3. Security/compliance gate
- AI-SEC approval required for policy or enforcement logic changes
- Change log entry required for any policy/model/prompt release
4. Deployment
- Blue/green deployment for generator and PEP path
- Rolling deployment for stateless API and monitoring components
5. Post-deploy verification
- 30-minute canary observation window
- Audit log completeness and latency checks must pass before full cutover

Rollback:
- One-command rollback to prior tagged release
- Previous model/prompt/policy artifacts retained for minimum 30 days
- Automated rollback trigger if policy evaluation failures or error rate breach threshold within first hour

---

## 6. Constraints & Assumptions

| Constraint | Source | Impact on Architecture |
|-----------|--------|----------------------|
| On-premises only | Hans Müller (CIO) | LLM must run on local GPU |
| €180K total budget | Board-approved | Limits hardware procurement |
| 6-month timeline | Board review August 2026 | Phased delivery required |
| EU AI Act compliance | Regulatory | Audit trail mandatory |
| 3 languages (EN/DE/CZ) | 8-country operation | Multilingual embedding + generation |
| 2,000 Confluence pages | Existing knowledge base | ~30% outdated, needs quality filter |

## 7. Architecture Decision Records

| # | Decision | Alternatives Considered | Rationale |
|---|----------|------------------------|-----------|
| ADR-001 | <!-- e.g., "Use YAML for policy format" --> | <!-- JSON, Rego, Markdown --> | <!-- Why YAML won --> |
| ADR-002 | <!-- e.g., "PEP after generation, not before" --> | <!-- Pre-generation filter --> | <!-- Why post-gen is better --> |
| ADR-003 | | | |

> Full ADR details in [architecture-decisions.md](architecture-decisions.md)

---

## 8. Risk Assessment (Architecture-Specific)

| Risk | Probability | Impact | Mitigation | Owner |
|------|------------|--------|-----------|-------|
| On-prem GPU insufficient for chosen LLM | Medium | Critical | Validate before model selection | FDE |
| ServiceNow API doesn't support required operations | Medium | High | API audit in Week 1 | AI-SE |
| Policy engine adds >500ms latency | Low | Medium | Performance testing in Sprint 1 | FDE + AI-SEC |
| Knowledge base quality degrades results | High | High | Quality filter + confidence threshold | AI-DS |

---

## Appendices

- [Interface Contracts — Detailed](interface-contracts.md)
- [Architecture Decision Records](architecture-decisions.md)
- [Data Flow Diagram](data-flow-diagram.md)
- [Deployment Model](deployment-model.md)
