# EU AI Act — Risk Classification Assessment
## EuroHealth AI Helpdesk System

**Assessor:** AI-SE
**Date:** 26 February 2026
**Regulation:** EU AI Act (Regulation 2024/1689)


## 1. System Description

| Field | Value |
|-------|-------|
| System name | EuroHealth AI IT Helpdesk |
| Purpose | Automated L1 ticket resolution + intelligent routing |
| Users | 12 helpdesk agents + ~5,000 employees (end users) |
| Data processed | IT knowledge base, ticket metadata, employee queries |
| Deployment | On-premises (EuroHealth data center) |
| Autonomy level | Human-in-the-loop (agent reviews before escalation) |

## 2. Risk Tier Assessment

### 2.1 Is this an Unacceptable Risk system? (Article 5)

| Criterion | Applies? | Evidence |
|----------|---------|---------|
| Social scoring | ☐ No | System does not score individuals |
| Subliminal manipulation | ☐ No | System provides information, not persuasion |
| Exploitation of vulnerabilities | ☐ No | Employees are not a vulnerable group in this context |
| Real-time biometric identification | ☐ No | No biometric data processed |

**Conclusion:** ☐ NOT unacceptable risk

### 2.2 Is this a High-Risk system? (Article 6 + Annex III)


| Annex III Category | Applies? | Reasoning |
|-------------------|---------|-----------|
| Biometric systems | ☐ No | |
| Critical infrastructure | ☐ No | IT helpdesk is operational support, not infrastructure control |
| Education/vocational training | ☐ No | |
| Employment & worker management | ☑ Yes | System routes and escalates employee IT tickets, affecting operational task allocation |
| Essential services access | ☐ No | Internal IT access support does not determine citizen access |
| Law enforcement | ☐ No | |
| Migration/border control | ☐ No | |
| Administration of justice | ☐ No | |

**Assessment:**

The EuroHealth AI Helpdesk qualifies as a HIGH-RISK system under Article 6 in conjunction with Annex III, Category 4 ("Employment, workers management and access to self-employment").

Reasoning:
- The system processes employee queries.
- It routes tickets affecting task allocation.
- It may influence access to IT systems required for employees to perform their duties.
- It operates across 8 EU countries, increasing regulatory exposure.

Therefore, full Articles 9–15 obligations apply.

## 2.3 If High-Risk — Required Obligations

| Obligation | Article | Status | Implementation |
|-----------|---------|--------|---------------|
| Risk management system | Art. 9 | In Progress | Risk register + monitoring |
| Data governance | Art. 10 | In Progress | KB quality audit + PII controls |
| Technical documentation | Art. 11 | In Progress | Solution Design + Governance Charter |
| Record-keeping (logging) | Art. 12 | In Progress | Audit logger + retention policy |
| Transparency | Art. 13 | In Progress | User notification ("AI-assisted") |
| Human oversight | Art. 14 | In Progress | HITL protocol + override |
| Accuracy, robustness, security | Art. 15 | In Progress | Golden dataset + security testing |

## 2.4 Role-Specific Accountability — AI-SE

As AI-SE, I am accountable for:

- Article 11 — Technical Documentation
- Article 12 — Record-Keeping / Logging
- Article 15 — Accuracy, Robustness & Cybersecurity (technical controls)

### Required Evidence (AI-SE)

| Article | Evidence Required | Source in Architecture | Governance Gap |
|----------|-----------------|------------------------|----------------|
| Art. 11 | Complete system documentation + traceability | docs/architecture/solution-design.md | No regulator-ready structured documentation pack |
| Art. 12 | Structured audit logs for every query, response, policy decision | governance/evidence/audit-log-schema.json | Retention period and tamper-evidence controls require formalization |
| Art. 15 | Security scanning, robustness testing, fallback mechanisms | CI/CD pipeline + guardrails | No defined security gate thresholds; no tamper-evidence logging |

Primary Gap:
Structured logging schema exists; however, immutable storage (WORM) and formal retention policy alignment with GDPR Art. 17 are not yet operationally enforced.

## 3. GPAI (General Purpose AI) Considerations

| Question | Answer |
|----------|--------|
| Are we using a GPAI model? | Yes — on-premises LLM deployed within EuroHealth infrastructure |
| Is the GPAI provider compliant? | As deployer, EuroHealth bears responsibility for Articles 9–15 obligations regardless of model origin |
| Do we need to document model capabilities/limitations? | Yes — documented in technical documentation per Art. 11 |

## 4. Timeline to Compliance

| Milestone | Target Date | Owner |
|----------|------------|-------|
| Risk classification confirmed | 26 Feb 2026 | AI-SEC |
| Evidence pack scope defined | 5 Mar 2026 | AI-SEC + AI-PM |
| Technical documentation complete | 30 Apr 2026 | ALL |
| Audit trail operational | 31 Mar 2026 | AI-SE |
| Human oversight protocol active | 31 Mar 2026 | AI-PM + AI-FE |
| Board-ready evidence pack | 31 July 2026 | AI-PM + AI-SEC |


## 5. Sign-off
Final Risk Tier Determination: HIGH-RISK


| Role | Determination | Name | Date |
|------|-------------|------|------|
| AI-SE | Technical compliance assessment completed | Praveen | 26 Feb 2026 |
| CISO | Review | Stefan Weber | |
| AI-PM | Acknowledged | | |
