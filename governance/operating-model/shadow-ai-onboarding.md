# Shadow AI Onboarding Process
## Bringing Ungoverned AI Systems Under Control

**Owner:** AI-SEC + AI-PM
**Context:** EuroHealth has at least 2 identified shadow AI systems (HR chatbot, Claims prototype)

---

## Process

### Step 1: Discovery & Registration
- Add system to [AI Inventory](../compliance/ai-inventory.md)
- Identify accountable owner
- Document: what data it processes, who uses it, what decisions it makes

### Step 2: Risk Assessment
- Classify under EU AI Act risk tier
- Assess PII exposure
- Evaluate governance gaps

### Step 3: Decision Gate (CIO)

| Decision | Criteria | Action |
|----------|---------|--------|
| **Onboard** | System is valuable AND can be governed | Migrate under central governance |
| **Sunset** | System is redundant OR cannot be governed | Decommission with migration plan |
| **Exception** | System is needed BUT governance timeline > 30 days | Time-bound exception, board-visible |

### Step 4: Onboarding (if decided)
- [ ] Connect to central audit logging
- [ ] Apply relevant policy YAML rules
- [ ] Add to monitoring dashboard
- [ ] Train system owner on governance requirements
- [ ] Schedule first compliance review

### Step 5: Ongoing Monitoring
- Monthly review of compliance status
- Quarterly risk re-assessment
