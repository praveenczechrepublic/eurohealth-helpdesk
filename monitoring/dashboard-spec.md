# Monitoring Dashboard Specification
## EuroHealth AI Helpdesk — Observability Design

**Owner:** AI-DA
**Consumers:** Helpdesk team (operational), CIO (executive), CISO (compliance)

---

## 1. Dashboard Views

### 1.1 Operational Dashboard (Helpdesk Team — Real-time)

| Metric | Source | Visualization | Alert Threshold |
|--------|--------|--------------|----------------|
| Active sessions | API Gateway | Counter | > 20 concurrent |
| Avg response latency | Pipeline logs | Line chart | > 3,000ms |
| Auto-resolve rate | Audit logs | Percentage gauge | < 30% (below target) |
| PEP block rate | Audit logs | Percentage | > 10% (anomaly) |
| Queue depth (awaiting human) | Escalation queue | Counter | > 5 |
| KB staleness warnings | Content freshness | Counter | > 20% of responses |

### 1.2 Executive Dashboard (CIO — Weekly/Monthly)

| Metric | Formula | Target |
|--------|---------|--------|
| Cost per ticket | total_cost / tickets_resolved | Decreasing trend |
| Escalation rate | escalated / total_queries | < <!-- target --> |
| Automation coverage | auto_resolved / total_queries | > <!-- target --> |
| Compliance readiness | checklist_items_done / total | 100% by August |
| User satisfaction | CSAT survey score | > <!-- target --> |

### 1.3 Compliance Dashboard (CISO — Weekly)

| Metric | Source | Purpose |
|--------|--------|---------|
| PII block events this week | PEP audit log | Prove PII controls work |
| Policy evaluation failures | PDP logs | Detect enforcement gaps |
| Audit log completeness | Log pipeline health | Prove logging is operational |
| Override rate trend | Override logs | Detect human trust issues |
| Open compliance items | Governance checklist | Track to August deadline |

## 2. KPI Definitions

<!-- AI-DA: Define the EXACT formula for each KPI -->

### Auto-Resolve Rate
```
auto_resolve_rate = (queries where decision="allow" AND no_override) / total_queries
```

### Escalation Rate
```
escalation_rate = (queries where decision="escalate" OR human_override) / total_queries
```

### Human Override Rate
```
override_rate = human_overrides / total_ai_responses
```

<!-- Continue for all KPIs... -->

## 3. Alerting Rules

<!-- AI-DA + AI-SE: Define when someone gets paged -->

| Alert | Condition | Severity | Notify |
|-------|----------|----------|--------|
| High latency | avg_latency > 5000ms for 5min | P2 | FDE |
| PII leak detected | pep_decision=allow AND pii_found_in_response | P0 | AI-SEC + CISO |
| Audit log gap | no_audit_entries for > 5min | P1 | AI-SE |
| Override spike | override_rate > 50% in 1hr | P2 | AI-PM |

## 4. Data Collection Points

<!-- Where in the pipeline do we capture metrics? -->

| Component | Metrics Emitted | Format |
|-----------|----------------|--------|
| API Gateway | request_count, latency, errors | <!-- Prometheus/JSON --> |
| Retriever | retrieval_time, chunks_found, relevance_scores | <!-- --> |
| Generator | generation_time, confidence, tokens_used | <!-- --> |
| PEP | decision_type, evaluation_time, policy_triggered | <!-- --> |
| Audit Logger | log_write_time, log_size | <!-- --> |
