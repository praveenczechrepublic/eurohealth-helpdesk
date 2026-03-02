# Incident Response Plan
## EuroHealth AI Helpdesk

**Owner:** AI-SEC
**Review cadence:** Monthly

---

## Severity Matrix

| Level | Definition | Response Time | Escalation |
|-------|-----------|--------------|------------|
| P0 | PII leak, compliance breach, data exfiltration | Immediate | CIO + CISO |
| P1 | System-wide malfunction, all responses incorrect | < 1 hour | AI-SE + FDE |
| P2 | Degraded performance, high latency | < 4 hours | FDE |
| P3 | Minor issue, workaround exists | Next business day | Assigned owner |

## Response Procedure

1. **Detect** — Alert from monitoring OR user/agent report
2. **Contain** — PEP defaults to BLOCK (fail-closed) if system integrity uncertain
3. **Investigate** — Reconstruct from audit logs
4. **Fix** — Root cause identified, patch applied
5. **Report** — Incident report within <!-- hours --> to CIO
6. **Prevent** — New test case added, policy updated if needed

## Post-Incident Checklist

- [ ] Audit log reviewed
- [ ] Root cause documented
- [ ] Golden dataset updated with failure case
- [ ] Policy rules updated if gap identified
- [ ] Incident report filed
- [ ] Stakeholders notified
