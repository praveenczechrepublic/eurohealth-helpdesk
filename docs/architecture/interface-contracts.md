# Interface Contracts
## Cross-Role API Specifications

**Version:** 0.1 DRAFT
**Status:** Day 13 Checkpoint 2 deliverable

---

## How to Use This Document

Each interface contract defines the boundary between two components owned by different roles. For each contract, specify:

1. **Provider** — who sends the data (role + component)
2. **Consumer** — who receives the data (role + component)
3. **Data format** — exact schema (JSON, YAML, etc.)
4. **Protocol** — how it's transmitted (REST, queue, file, internal call)
5. **Error handling** — what happens when it fails
6. **SLA** — response time expectations

---

## Contract 1: User Query → Retriever

**Provider:** AI-FE (User Interface)
**Consumer:** FDE (Retriever)

```json
// REQUEST
{
  "query": "How do I reset my VPN password?",
  "language": "en",
  "session_id": "sess-abc123",
  "user_id": "emp-00456",
  "timestamp": "2026-03-15T14:32:00Z"
}
```

```json
// RESPONSE (from Retriever)
{
  "query": "...",
  "chunks": [
    {
      "source": "confluence/it/vpn-setup-guide.html",
      "content": "To reset your VPN password...",
      "relevance_score": 0.92,
      "language": "en",
      "last_updated": "2026-01-15"
    }
  ],
  "retrieval_time_ms": 45
}
```

**Error handling:**
- If vector DB is unreachable, return `retriever_unavailable` to API Gateway; API responds with escalation handoff message and logs `system_error`.
- If no relevant chunks pass threshold, return empty `chunks` with `retrieval_time_ms`; generator must switch to low-confidence mode and trigger escalation policy path.

**SLA:**
- Target retriever latency: <= 250ms
- 99th percentile retriever latency: <= 500ms

---

## Contract 2: Retriever + Query → Generator (LLM)

**Provider:** FDE (Retriever)
**Consumer:** FDE (Generator)

```json
// INPUT TO LLM
{
  "query": "...",
  "context_chunks": [ /* from retriever */ ],
  "system_prompt": "You are a helpful IT helpdesk assistant for EuroHealth...",
  "language": "en",
  "max_tokens": 500
}
```

```json
// LLM OUTPUT (before PEP)
{
  "response_draft": "To reset your VPN password, go to...",
  "confidence": 0.88,
  "tokens_used": 127,
  "model_version": "llama-3.2-8b-v1",
  "generation_time_ms": 340
}
```

---

## Contract 3: Generator → PEP (Policy Enforcement)

**Provider:** FDE (Generator)
**Consumer:** AI-SEC (Policy Enforcement Point)

```json
// PEP INPUT
{
  "query": "...",
  "response_draft": "...",
  "confidence": 0.88,
  "context_sources": ["confluence/it/vpn-setup-guide.html"],
  "user_id": "emp-00456",
  "session_id": "sess-abc123"
}
```

```json
// PEP OUTPUT — ALLOW
{
  "decision": "allow",
  "response": "To reset your VPN password, go to...",
  "policies_evaluated": ["pii-protection", "scope-limitation"],
  "evaluation_time_ms": 12
}
```

```json
// PEP OUTPUT — BLOCK
{
  "decision": "block",
  "policy": "pii-protection",
  "rule": "block-salary-data",
  "original_response_hash": "a3f8c2...",
  "substitute_response": "I cannot share personal salary information. Please contact HR.",
  "pii_detected": ["salary", "personal_id"],
  "escalate_to": "human_agent",
  "evaluation_time_ms": 15
}
```
**Error Handling:**
- If PDP evaluation fails or exceeds latency threshold (200ms configurable), PEP defaults to `block` and escalates to human review.
- No response may bypass PEP enforcement.

**SLA:**
- Target policy evaluation latency: ≤ 200ms
- 99th percentile must remain under 300ms under normal load
---

## Contract 4: PEP → Audit Logger

**Provider:** AI-SEC (PEP)
**Consumer:** AI-SE (Audit Logger)

```json
// AUDIT LOG ENTRY (every PEP decision, allow AND block)
{
  "timestamp": "2026-03-15T14:32:01.234Z",
  "event_type": "pep_decision",
  "session_id": "sess-abc123",
  "user_id": "emp-00456",
  "query_hash": "sha256:...",
  "decision": "block",
  "policy": "pii-protection",
  "rule": "block-salary-data",
  "pii_types": ["salary", "personal_id"],
  "escalated_to": "human_agent",
  "model_version": "llama-3.2-8b-v1",
  "confidence": 0.88,
  "latency_ms": {
    "retrieval": 45,
    "generation": 340,
    "policy_evaluation": 15,
    "total": 412
  }
}
```

**Retention:** Minimum 3 years (EU AI Act Article 12 compliance)
**Storage:** On-prem encrypted object storage (`audit-logs`) with immutable daily snapshots, RBAC-restricted access, and checksum verification on write/read.
**Reconstruction SLA:** Full decision reconstruction available within 24 hours upon regulatory request.

---

## Contract 5: Pipeline → Monitoring

**Provider:** ALL pipeline components
**Consumer:** AI-DA (Monitoring Dashboard)

```json
// METRICS PAYLOAD (aggregated per minute)
{
  "timestamp": "2026-03-15T14:32:00Z",
  "queries_total": 12,
  "queries_allowed": 10,
  "queries_blocked": 1,
  "queries_escalated": 1,
  "avg_confidence": 0.85,
  "avg_latency_ms": 380,
  "languages": {"en": 7, "de": 3, "cz": 2},
  "top_blocked_policy": "pii-protection"
}
```

---

## Contract 6: PEP → User Interface (Block/Redirect States)

**Provider:** AI-SEC (PEP via API Gateway)
**Consumer:** AI-FE (User Interface)

<!-- 
AI-FE: What does the user SEE when:
- Response is allowed? (normal display)
- Response is blocked? (what message, what options?)
- User is escalated to human? (handoff UX)
- System confidence is low? (warning indicator?)
-->

---

## Contract 7: User Interface → Human Override

**Provider:** AI-FE (Override Button)
**Consumer:** AI-SE (Override Logger) + AI-PM (Escalation Queue)

```json
// OVERRIDE EVENT
{
  "timestamp": "...",
  "session_id": "...",
  "agent_id": "jan-kovar",
  "override_type": "reject_ai_response",
  "reason": "Response was technically correct but inappropriate tone for this customer",
  "original_response_hash": "...",
  "replacement_response": "...(agent's manual response)..."
}
```

**Error handling:**
- If override log write fails, UI displays `override_pending_sync` status and retries asynchronously up to 3 times.
- If retries fail, raise P1 alert to AI-SE and place event in durable local queue for replay.

**SLA:**
- Override event write acknowledgement: <= 2 seconds
- Override event durability confirmation in central audit store: <= 60 seconds

<!-- This data feeds AI-DA dashboards: override rate, override reasons, agent patterns -->
