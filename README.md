# EuroHealth AI Helpdesk — Industrialization Initiative

**Client:** EuroHealth Insurance AG
**Sponsor:** Hans Müller, CIO
**Engagement:** AI Helpdesk Industrialization
**Budget:** €180,000 | **Timeline:** 6 months (target: August 2026 board review)
**Constraint:** On-premises deployment only

---

## Project Summary

<!-- AI-PM: Write 3-4 sentences. What are we doing, why, and what does success look like? -->

## Team

| Role | Name | Primary Responsibility |
|------|------|----------------------|
| FDE | | Pipeline architecture, infrastructure validation |
| AI-SE | | Deployment, CI/CD, logging infrastructure |
| AI-SEC | | Governance, compliance, policy enforcement |
| AI-PM | | Delivery planning, stakeholder management, budget |
| AI-DA | | Metrics, dashboards, board reporting |
| AI-DS | | Data quality, evaluation framework, golden dataset |
| AI-FE | | User interface, streaming UX, HITL design |

## Project Structure

```
docs/           → Delivery artifacts (what the client receives)
governance/     → Governance artifacts (what makes it auditable)
src/            → Technical artifacts (what actually runs)
tests/          → Quality assurance (how we prove it works)
monitoring/     → Observability (how we know it's healthy)
```

## Current Phase

- [x] Phase 1: Discovery (Day 11-12)
- [ ] Phase 2: Co-Design / Architecture (Day 13-14) ← **WE ARE HERE**
- [ ] Phase 3: Build (Day 15+)
- [ ] Phase 4: Verify
- [ ] Phase 5: Release
- [ ] Phase 6: Roadmap to Operate

## Key Documents

| Document | Status | Owner |
|----------|--------|-------|
| [Consolidated Discovery Report](docs/discovery/consolidated-discovery-report.md) | 🔴 Draft | AI-PM + ALL |
| [Solution Design](docs/architecture/solution-design.md) | 🔴 Draft | FDE + AI-SE |
| [Interface Contracts](docs/architecture/interface-contracts.md) | 🔴 Draft | ALL |
| [Governance Charter](governance/operating-model/governance-charter.md) | 🔴 Not started | AI-SEC + AI-PM |
| [EU AI Act Classification](governance/compliance/eu-ai-act-classification.md) | 🔴 Not started | AI-SEC |
| [Risk Register](docs/project-plan/risk-register.md) | 🔴 Draft | AI-PM |
