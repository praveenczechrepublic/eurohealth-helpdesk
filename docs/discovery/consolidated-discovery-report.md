# Consolidated Discovery Report
## EuroHealth Insurance AG — AI Helpdesk Industrialization

**Version:** 1.0 DRAFT
**Date:** <!-- date -->
**Authors:** All roles (consolidated by AI-PM)
**Status:** Co-Design input document

---

## 1. Unified Executive Summary

<!-- 
AI-PM: Synthesize all 7 discovery reports into 3-4 paragraphs.
Answer these questions:
- What did the client ask for?
- What did we actually find?
- What changes our approach?
- What must happen before we can build?
-->

## 2. Stakeholder Map

<!-- Merge all role perspectives into ONE stakeholder view -->

| Stakeholder | Role | Power | Interest | Key Quote | Risk |
|------------|------|-------|----------|-----------|------|
| Hans Müller | CIO / Sponsor | High | High | | |
| Stefan Weber | CISO | High | Medium | | |
| Jan Kovář | Helpdesk Lead | Low | High | | |
| HR Department | Shadow AI Owner | Medium | Low | | |
| Claims Department | Shadow AI Owner | Medium | Low | | |
| Board of Directors | Oversight | Highest | Variable | | |

## 3. Translation Table — What Was Said vs. What It Means

<!-- AI-PM + ALL: Merge the best "translation" insights from each role report -->

| What Hans Said | What He Didn't Say | What It Actually Means | Implication for Architecture |
|---------------|-------------------|----------------------|----------------------------|
| "Cut costs by 30%." | | | |
| "Everyone's doing their own thing." | | | |
| "On-prem only." | | | |
| "EU AI Act compliance before deadline." | | | |
| "35% already automated." | | | |
| "If this works for IT, Claims wants it too." | | | |

## 4. Confirmed Findings — Cross-Role Consensus

<!-- List findings that ALL roles independently confirmed -->

### 4.1 This is a governance initiative, not a chatbot project
<!-- Evidence from each role's report that supports this -->

### 4.2 Shadow AI creates uncontrolled regulatory exposure
<!-- Which roles found this, what specifically -->

### 4.3 Knowledge base quality is a commercial risk
<!-- ~30% outdated — who confirmed, what impact -->

### 4.4 On-prem constraint gates the entire architecture
<!-- Infrastructure implications from FDE/AI-SE perspective -->

### 4.5 Adoption risk is financially material
<!-- How helpdesk team resistance affects ROI — AI-PM/AI-DA/AI-FE views -->

## 5. Open Questions — Requiring Validation

<!-- Things we believe but haven't confirmed. Each needs an owner and deadline. -->

| # | Question | Why It Matters | Owner | Target Date |
|---|----------|---------------|-------|-------------|
| 1 | Is the 35% automation baseline validated? | ROI model depends on it | AI-DA | Week 1 |
| 2 | What GPU capacity exists on-prem? | Gates LLM selection | FDE | Week 1 |
| 3 | What's the actual ServiceNow API capability? | Determines integration scope | AI-SE | Week 1 |
| 4 | What EU AI Act risk tier applies? | Determines compliance scope | AI-SEC | Week 1 |
| 5 | What's the KB content ownership model? | Quality fix needs an owner | AI-DS | Week 1 |

## 6. Critical Gaps — What Must Be Built

<!-- Things that definitively DO NOT EXIST at EuroHealth today -->

| Gap | Impact If Not Addressed | Owner | Priority |
|-----|------------------------|-------|----------|
| No AI inventory / registry | Cannot demonstrate governance to board | AI-SEC | P0 |
| No policy enforcement mechanism | PII leak risk, regulatory exposure | AI-SEC + FDE | P0 |
| No centralized audit logging | Cannot reconstruct decisions for EU AI Act | AI-SE | P0 |
| No structured metrics/dashboards | Board has no visibility into AI performance | AI-DA | P1 |
| No formal escalation protocol | Human override is ad-hoc, untracked | AI-PM + AI-FE | P1 |
| No evaluation framework | Cannot prove system quality or detect drift | AI-DS | P1 |

## 7. Priority Decision — What Gets Built First

<!-- 
AI-PM: Based on all findings, define the Phase 1 scope.
Use the compliance > governance > ROI > expansion hierarchy.
-->

### Phase 0 — Governance & Feasibility Gate (Weeks 1-4)

Deliverables:
1. <!-- AI-SEC: AI inventory + risk classification -->
2. <!-- FDE: On-prem infrastructure validation -->
3. <!-- AI-DA: Baseline cost and escalation model -->
4. <!-- AI-PM: Governance operating model draft -->

**Go/No-Go criteria for Phase 1:**
- [ ] Infrastructure feasible within budget
- [ ] Risk tier classification confirmed
- [ ] Escalation baseline measurable
- [ ] Evidence pack scope defined and agreed

### Phase 1 — Escalation Reduction & Control (Months 2-4)

<!-- Scope: what gets built, what's explicitly OUT of scope -->

### Phase 2 — Consolidation & Board Rehearsal (Months 4-6)

<!-- What happens in the final push before August -->

## 8. Cross-Role Dependencies

<!-- From Day 12 individual reports — now formalized -->

| Provider Role | Consumer Role | What They Need | Format | When |
|--------------|--------------|---------------|--------|------|
| AI-SEC | FDE | Audit logging requirements | Markdown spec | Week 1 |
| FDE | AI-SE | Infrastructure constraints | Architecture doc | Week 1 |
| AI-DS | AI-SE | KB quality assessment | JSON report | Week 1 |
| AI-DA | AI-PM | Baseline cost model | Dashboard + CSV | Week 2 |
| AI-SEC | AI-FE | Policy block/redirect states | YAML + API spec | Week 2 |
| AI-PM | ALL | Budget allocation per workstream | Approved plan | Week 1 |
| FDE | AI-FE | Streaming response API contract | OpenAPI spec | Week 2 |

## 9. Budget Allocation (Initial)

| Workstream | Allocation | Rationale |
|-----------|-----------|-----------|
| Governance & Compliance | €45,000 (25%) | Board-critical milestone |
| On-Prem Validation | €27,000 (15%) | Gating feasibility |
| Escalation Reduction | €54,000 (30%) | Primary ROI driver |
| Monitoring & Audit | €18,000 (10%) | Compliance proof |
| Change Management | €18,000 (10%) | Protect ROI realization |
| Reporting & Metrics | €18,000 (10%) | Board-facing KPI visibility |

## 10. Recommendation

<!-- AI-PM: 2-3 paragraphs. What do we recommend to Hans? -->

---

**Sign-off:**

| Role | Name | Approved | Date |
|------|------|----------|------|
| AI-PM | | ☐ | |
| FDE | | ☐ | |
| AI-SE | | ☐ | |
| AI-SEC | | ☐ | |
| AI-DA | | ☐ | |
| AI-DS | | ☐ | |
| AI-FE | | ☐ | |
