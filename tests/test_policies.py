import json
import logging

from src.policy_engine import PolicyDecision, PolicyDecisionPoint, PolicyEnforcementPoint


class StubPDP:
    def __init__(self, decision: PolicyDecision):
        self._decision = decision

    def evaluate(self, query: str, response: str, confidence: float) -> PolicyDecision:
        return self._decision


def _audit_payloads(caplog):
    payloads = []
    for record in caplog.records:
        message = record.getMessage()
        if message.startswith("AUDIT_EVENT "):
            payloads.append(json.loads(message[len("AUDIT_EVENT ") :]))
    return payloads


def test_allow_decision_logs_structured_audit_event(caplog):
    pep = PolicyEnforcementPoint(StubPDP(PolicyDecision(action="allow")))
    query = "How do I reset my VPN password?"
    response = "Open the VPN portal and click reset."

    with caplog.at_level(logging.INFO, logger="policy_engine"):
        result = pep.enforce(
            query,
            response,
            0.92,
            session_id="sess-123",
            user_id="emp-42",
            model_version="llama-3.2-8b-v1",
            latency_ms={"retrieval": 45, "generation": 340},
            sources_used=["confluence/it/vpn-setup-guide.html"],
        )

    assert result == response
    payloads = _audit_payloads(caplog)
    assert len(payloads) == 1
    event = payloads[0]
    assert event["event_type"] == "pep_decision"
    assert event["decision"] == "allow"
    assert event["session_id"] == "sess-123"
    assert event["user_id"] == "emp-42"
    assert event["query_hash"].startswith("sha256:")
    assert event["policy"] is None
    assert event["rule"] is None
    assert event["latency_ms"]["retrieval"] == 45
    assert event["latency_ms"]["generation"] == 340
    assert "policy_evaluation" in event["latency_ms"]
    assert event["latency_ms"]["total"] >= 385
    assert event["sources_used"] == ["confluence/it/vpn-setup-guide.html"]


def test_block_with_escalation_logs_decision_and_escalation_events(caplog):
    decision = PolicyDecision(
        action="block",
        policy_name="pii-protection",
        rule_id="block-salary-data",
        substitute_response=(
            "I cannot share personal salary info. Please contact HR."
        ),
        escalate_to="human_agent",
    )
    pep = PolicyEnforcementPoint(StubPDP(decision))

    with caplog.at_level(logging.INFO, logger="policy_engine"):
        result = pep.enforce(
            "What is Alex's salary?",
            "Alex earns 120K.",
            0.88,
            session_id="sess-pii",
            model_version="llama-3.2-8b-v1",
            pii_types=["salary", "personal_id"],
            latency_ms={"policy_evaluation": 12, "total": 397},
        )

    assert "cannot share personal salary" in result
    payloads = _audit_payloads(caplog)
    assert len(payloads) == 2
    decision_event, escalation_event = payloads

    assert decision_event["event_type"] == "pep_decision"
    assert decision_event["decision"] == "block"
    assert decision_event["policy"] == "pii-protection"
    assert decision_event["rule"] == "block-salary-data"
    assert decision_event["escalated_to"] == "human_agent"
    assert decision_event["pii_types"] == ["salary", "personal_id"]

    assert escalation_event["event_type"] == "escalation"
    assert escalation_event["decision"] == "block"
    assert escalation_event["escalated_to"] == "human_agent"
    assert escalation_event["session_id"] == "sess-pii"


def test_latency_defaults_when_not_provided(caplog):
    pep = PolicyEnforcementPoint(StubPDP(PolicyDecision(action="allow")))

    with caplog.at_level(logging.INFO, logger="policy_engine"):
        pep.enforce("Ping", "Pong", 0.81, session_id="sess-latency")

    payloads = _audit_payloads(caplog)
    assert len(payloads) == 1
    latency = payloads[0]["latency_ms"]
    assert "policy_evaluation" in latency
    assert "total" in latency
    assert isinstance(latency["policy_evaluation"], int)
    assert isinstance(latency["total"], int)


def test_pdp_minimal_pii_protection_rule_evaluation():
    pdp = PolicyDecisionPoint("governance/policies")
    decision = pdp.evaluate(
        query="What is my manager salary?",
        response="John Smith monthly salary is 10000 EUR and personal_id 123456/7890.",
        confidence=0.9,
    )

    assert decision.action == "block"
    assert decision.policy_name == "pii-protection"
    assert decision.rule_id == "block-salary-data"
    assert decision.escalate_to == "human_agent"
    assert "salary" in (decision.pii_types or [])
