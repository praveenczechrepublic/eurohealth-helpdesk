# AI Governance Charter
## EuroHealth Insurance AG

**Version:** 0.1 DRAFT
**Owner:** AI-SEC + AI-PM
**Status:** Pending CIO approval

---

## 1. Purpose

This charter establishes the governance framework for all AI systems at EuroHealth Insurance AG. It defines ownership, decision rights, enforcement mechanisms, and compliance requirements.

<!-- AI-SEC: Why does this document exist? What problem does it solve? -->

## 2. Scope

This charter applies to:
- [ ] IT Helpdesk AI agent (primary system)
- [ ] HR chatbot (shadow AI — to be onboarded or sunset)
- [ ] Claims LangChain prototype (shadow AI — to be onboarded or sunset)
- [ ] Any future AI system deployed at EuroHealth

## 3. AI Inventory — System Registry

<!-- AI-SEC: This is the MANDATORY registry. Every AI system must be listed. -->

| System | Department | Owner | Risk Tier | Status | Registered |
|--------|-----------|-------|-----------|--------|-----------|
| Moveworks (IT helpdesk) | IT | Jan Kovář | <!-- --> | Active | ☐ |
| HR Chatbot | HR | <!-- unknown --> | <!-- --> | Active (ungoverned) | ☐ |
| Claims LangChain | Claims | <!-- unknown --> | <!-- --> | Prototype (ungoverned) | ☐ |
| AI Helpdesk (new) | IT | <!-- --> | <!-- --> | Design phase | ☐ |

**Rule:** Any AI system not in this registry by <!-- date --> is subject to mandatory sunset or exception process.

## 4. Decision Rights

## 4. Decision Rights

| Decision | Who Decides | Who Is Consulted | Who Is Informed |
|----------|------------|-----------------|----------------|
| AI system goes to production | AI-PM | AI-SEC, AI-SE | CIO |
| Policy rule is added/changed | AI-SEC | AI-PM, AI-SE | AI-DA |
| Human override is triggered | Helpdesk Agent | AI-FE | AI-DA |
| AI system is sunset | CIO | AI-PM, AI-SEC | All stakeholders |
| Budget reallocation | CIO | AI-PM | Finance |
| Incident response activation | AI-SEC | AI-SE, AI-PM | CISO |
| Changes to audit-log-schema.json | AI-SE | AI-SEC, AI-PM | AI-DA |
| Log retention period change | AI-SEC | AI-SE, DPO | AI-PM |

## 5. Policy Enforcement Model

### 5.1 Policy-as-Code

All governance rules are expressed as machine-readable YAML files stored in `governance/policies/`. Policies are:
- Version-controlled in Git
- Validated on every commit (CI/CD)
- Enforced at runtime by the Policy Enforcement Point (PEP)
- Auditable (every evaluation logged)

### 5.2 Policy Categories

| Category | File | Purpose |
|---------|------|---------|
| PII Protection | `policies/pii-protection.yaml` | Block personal data from AI responses |
| Scope Limitation | `policies/scope-limitation.yaml` | Keep AI within approved topic boundaries |
| Escalation Rules | `policies/escalation-rules.yaml` | Define when AI must hand off to human |
| Data Retention | `policies/data-retention.yaml` | How long data is kept, where, why |
| Content Freshness | `policies/content-freshness.yaml` | Detect and flag outdated knowledge base content |

### 5.3 Policy Change Process

1. Proposed change → Pull request with YAML diff
2. AI-SEC review → Compliance impact assessment
3. AI-PM approval → Business impact confirmation
4. Merge → Automated deployment to PDP
5. Audit log → Change recorded with timestamp and author
Additional Rule (Audit Logging Changes):
Any modification to `audit-log-schema.json` requires:
- Version increment
- CI schema validation
- AI-SEC approval (security review)
- Documentation update referencing Art. 11 and Art. 12

## 6. Human Oversight Protocol

<!-- Refer to: operating-model/human-override-protocol.md -->

### 6.1 When Must a Human Be Involved?

- [ ] AI confidence below <!-- threshold -->
- [ ] PEP blocks a response (human agent takes over)
- [ ] User explicitly requests human
- [ ] Query involves sensitive categories: <!-- list -->
- [ ] Same user repeats query 3+ times

### 6.2 Override Tracking

Every human override is logged with:
- Agent ID, timestamp, session ID
- Override type (reject/edit/escalate)
- Reason (free text)
- Original AI response hash

Override patterns are reviewed weekly by AI-DA.

## 7. Compliance Requirements

### 7.1 EU AI Act Obligations

<!-- AI-SEC: Based on risk classification from eu-ai-act-classification.md -->

| Requirement | Article | Implementation | Status |
|------------|---------|---------------|--------|
| Risk classification | Art. 6 | `governance/compliance/eu-ai-act-classification.md` | ☑ Completed |
| Technical documentation | Art. 11 | Solution Design + this Charter | ☑ In Progress |
| Record-keeping | Art. 12 | `governance/evidence/audit-log-schema.json` | ☑ Implemented |
| Transparency | Art. 13 | User interface disclosure | ☐ Pending |
| Human oversight | Art. 14 | HITL protocol + override tracking | ☑ Implemented |
| Accuracy & robustness | Art. 15 | Golden dataset + evaluation framework | ☐ In Progress |

### 7.2 GDPR Obligations

| Requirement | Implementation | Status |
|------------|---------------|--------|
| Data Protection Impact Assessment | `governance/compliance/data-protection-impact.md` | ☐ |
| PII handling controls | `governance/policies/pii-protection.yaml` | ☐ |
| Data subject rights | <!-- how can an employee request deletion? --> | ☐ |
| Data retention limits | `governance/policies/data-retention.yaml` | ☐ |

## 8. Incident Response

<!-- AI-SEC: What happens when something goes wrong? -->

### 8.1 Severity Levels

| Level | Definition | Response Time | Example |
|-------|-----------|--------------|---------|
| P0 — Critical | PII leaked, compliance breach | Immediate | PEP bypassed, salary data exposed |
| P1 — High | System malfunction affecting users | < 1 hour | Generator hallucinating, all responses wrong |
| P2 — Medium | Degraded performance | < 4 hours | Response latency >5s |
| P3 — Low | Minor issue, workaround exists | Next business day | Dashboard metric incorrect |

### 8.2 Incident Process

1. **Detect** — Monitoring alert OR user report
2. **Contain** — Disable affected component (PEP fails-closed by default)
3. **Investigate** — Audit log reconstruction
4. **Fix** — Root cause + policy/code change
5. **Report** — Incident report to CIO within <!-- hours -->
6. **Prevent** — Add test case to golden dataset + update policy if needed

### 8.3 Audit Logging Failure Protocol (AI-SE Domain)

Regulatory Basis: EU AI Act Art. 12 (Record-keeping), Art. 15 (Robustness)

Trigger Conditions:
- Audit completeness drops below 99.5%
- Logging pipeline unavailable > 5 minutes
- Tamper-evidence checksum mismatch detected

Escalation Timeline:

Within 5 minutes:
- AI-SE notified automatically
- AI-SEC notified
- CI/CD deployments frozen

Within 30 minutes:
- AI-PM notified
- System shifts to supervised-only mode (no autonomous escalation)

Within 4 hours:
- CISO notified
- Incident report drafted
- Reconstruction test executed

Fallback Behavior:
If structured logging is unavailable, AI Helpdesk may only operate in human-review mode until logging integrity is restored.

Quarterly Requirement:
A reconstruction drill must be performed simulating a historical audit request ("March 15, 14:32").

## 9. Reporting Cadence

| Report | Audience | Frequency | Owner |
|--------|----------|-----------|-------|
| Operational dashboard | Helpdesk team | Real-time | AI-DA |
| Weekly governance evidence | CISO | Weekly | AI-SEC |
| Board metrics summary | CIO / Board | Monthly | AI-PM + AI-DA |
| Compliance status | CISO + Legal | Monthly | AI-SEC |
| August evidence pack | Board | One-time (Month 5) | AI-PM + AI-SEC |

---

**Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| CIO (Sponsor) | Hans Müller | | |
| CISO | Stefan Weber | | |
| AI-PM | | | |
| AI-SEC | | | |
