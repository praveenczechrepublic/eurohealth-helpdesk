# Human Override Protocol
## EuroHealth AI Helpdesk — Human-in-the-Loop Design

**Owner:** AI-PM + AI-FE
**KAF Layer:** Layer 5 — Human-in-the-Loop Controls

---

## 1. Override Triggers

| Trigger | Automatic? | Who Acts |
|---------|-----------|----------|
| PEP blocks response | Yes | Human agent takes over session |
| AI confidence below threshold | Yes | Response flagged for agent review |
| User requests human | Yes | Immediate handoff |
| 3+ repeated queries in session | Yes | Agent notified |
| Agent clicks override button | Manual | Agent replaces AI response |

## 2. Override Types

| Type | Description | Logged As |
|------|------------|----------|
| **Reject** | Agent discards AI response, writes own | `reject_ai_response` |
| **Edit** | Agent modifies AI response before sending | `edit_ai_response` |
| **Escalate** | Agent escalates to L2/specialist | `manual_escalation` |
| **Approve** | Agent confirms AI response is correct | `approve_ai_response` |

## 3. UX Requirements

<!-- AI-FE: Design these elements -->

### 3.1 Agent View
- AI response shown as **draft** (not sent automatically)
- Confidence indicator visible (green/yellow/red)
- One-click override button
- Reason dropdown + free text field
- Session history visible

### 3.2 End-User View
- <!-- Does the user know they're talking to AI? (EU AI Act Art. 13: YES) -->
- <!-- What does the user see when PEP blocks? -->
- <!-- What does the handoff to human look like? -->

## 4. Override Monitoring

<!-- AI-DA: These metrics feed your dashboard -->

| Metric | Formula | Target | Alert Threshold |
|--------|---------|--------|----------------|
| Override rate | overrides / total_responses | <!-- --> | <!-- --> |
| Override by type | count per type / total_overrides | <!-- --> | <!-- --> |
| Override by agent | count per agent / agent_total | <!-- --> | <!-- --> |
| Top override reasons | grouped by reason text | <!-- --> | <!-- --> |
