"""
EuroHealth AI Helpdesk — Policy Engine (PDP/PEP)
=================================================
PDP = reads policy YAML files, evaluates rules, returns decision
PEP = sits in the pipeline, calls PDP, enforces the decision

Architecture:
    User Query → Retriever → LLM → [PEP] → Response
                                      ↑
                                    [PDP] ← policies/*.yaml
"""

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger("policy_engine")


@dataclass
class PolicyDecision:
    action: Literal["allow", "block", "redirect", "escalate", "redact"]
    policy_name: str | None = None
    rule_id: str | None = None
    substitute_response: str | None = None
    escalate_to: str | None = None
    pii_types: list[str] | None = None


class PolicyDecisionPoint:
    """Reads YAML rules, evaluates, decides. Does NOT enforce."""

    def __init__(self, policies_dir: str = "governance/policies/"):
        self.policies = self._load_policies(policies_dir)

    def _load_policies(self, policies_dir: str) -> list[dict]:
        policies = []
        for f in Path(policies_dir).glob("*.yaml"):
            with open(f) as fh:
                policies.append(yaml.safe_load(fh))
        return policies

    def evaluate(self, query: str, response: str, confidence: float) -> PolicyDecision:
        # Minimal runtime enforcement path: pii-protection keyword matching.
        response_text = response.casefold()
        for policy in self.policies:
            policy_meta = policy.get("policy", {})
            if policy_meta.get("name") != "pii-protection":
                continue

            for rule in policy.get("rules", []):
                matched_terms = self._match_response_contains(
                    rule_expression=str(rule.get("if", "")),
                    response_text=response_text,
                )
                if not matched_terms:
                    continue

                return PolicyDecision(
                    action=rule.get("then", "block"),
                    policy_name=policy_meta.get("name"),
                    rule_id=rule.get("id"),
                    substitute_response=rule.get("substitute_response"),
                    escalate_to=rule.get("escalate_to"),
                    pii_types=matched_terms,
                )

        return PolicyDecision(action="allow")

    @staticmethod
    def _match_response_contains(rule_expression: str, response_text: str) -> list[str]:
        """
        Parses expressions like:
            response.contains(salary, compensation, personal_id)
        and returns the matched terms.
        """
        expr = rule_expression.strip()
        if not expr.startswith("response.contains(") or not expr.endswith(")"):
            return []

        inner = expr[len("response.contains(") : -1]
        candidates = [token.strip().casefold() for token in inner.split(",") if token.strip()]
        return [term for term in candidates if term in response_text]


class PolicyEnforcementPoint:
    """Sits in pipeline. Calls PDP. Enforces. Logs."""

    def __init__(self, pdp: PolicyDecisionPoint):
        self.pdp = pdp

    def enforce(
        self,
        query: str,
        response: str,
        confidence: float,
        *,
        session_id: str = "unknown-session",
        user_id: str | None = None,
        model_version: str = "unknown-model",
        latency_ms: dict | None = None,
        sources_used: list[str] | None = None,
        pii_types: list[str] | None = None,
    ) -> str:
        started = time.perf_counter()
        decision = self.pdp.evaluate(query, response, confidence)
        policy_eval_ms = int((time.perf_counter() - started) * 1000)
        normalized_latency = self._normalize_latency(latency_ms, policy_eval_ms)
        query_hash = self._hash_query(query)

        self._log_event(
            self._build_audit_event(
                event_type="pep_decision",
                session_id=session_id,
                user_id=user_id,
                query_hash=query_hash,
                decision=decision.action,
                policy=decision.policy_name,
                rule=decision.rule_id,
                pii_types=pii_types or decision.pii_types or [],
                escalated_to=decision.escalate_to,
                model_version=model_version,
                confidence=confidence,
                latency_ms=normalized_latency,
                sources_used=sources_used or [],
            )
        )

        if decision.action == "allow":
            return response
        if decision.action == "block":
            if decision.escalate_to:
                self._escalate(
                    session_id=session_id,
                    user_id=user_id,
                    query_hash=query_hash,
                    decision_action=decision.action,
                    target=decision.escalate_to,
                    model_version=model_version,
                    confidence=confidence,
                    latency_ms=normalized_latency,
                )
            return decision.substitute_response or "I cannot process this request."
        if decision.action == "escalate":
            self._escalate(
                session_id=session_id,
                user_id=user_id,
                query_hash=query_hash,
                decision_action=decision.action,
                target=decision.escalate_to or "human_agent",
                model_version=model_version,
                confidence=confidence,
                latency_ms=normalized_latency,
            )
            return decision.substitute_response or "Connecting you with a human agent."
        return "I cannot process this request. Please contact IT support."

    def _normalize_latency(self, latency_ms: dict | None, policy_eval_ms: int) -> dict:
        raw = dict(latency_ms or {})
        raw["policy_evaluation"] = int(raw.get("policy_evaluation", policy_eval_ms))

        if "total" in raw:
            raw["total"] = int(raw["total"])
            return raw

        total = 0
        for key in ("retrieval", "generation", "policy_evaluation"):
            if key in raw and raw[key] is not None:
                total += int(raw[key])
        raw["total"] = total if total > 0 else int(policy_eval_ms)
        return raw

    def _build_audit_event(
        self,
        *,
        event_type: Literal["pep_decision", "escalation", "system_error"],
        session_id: str,
        user_id: str | None,
        query_hash: str,
        decision: Literal["allow", "block", "redirect", "escalate", "redact"],
        policy: str | None,
        rule: str | None,
        pii_types: list[str],
        escalated_to: str | None,
        model_version: str,
        confidence: float,
        latency_ms: dict,
        sources_used: list[str],
    ) -> dict:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "event_type": event_type,
            "session_id": session_id,
            "user_id": user_id,
            "query_hash": query_hash,
            "decision": decision,
            "policy": policy,
            "rule": rule,
            "pii_types": pii_types,
            "escalated_to": escalated_to,
            "model_version": model_version,
            "confidence": confidence,
            "latency_ms": latency_ms,
            "sources_used": sources_used,
        }

    def _log_event(self, payload: dict) -> None:
        logger.info("AUDIT_EVENT %s", json.dumps(payload, sort_keys=True))

    def _escalate(
        self,
        *,
        session_id: str,
        user_id: str | None,
        query_hash: str,
        decision_action: Literal["allow", "block", "redirect", "escalate", "redact"],
        target: str,
        model_version: str,
        confidence: float,
        latency_ms: dict,
    ) -> None:
        self._log_event(
            self._build_audit_event(
                event_type="escalation",
                session_id=session_id,
                user_id=user_id,
                query_hash=query_hash,
                decision=decision_action,
                policy=None,
                rule=None,
                pii_types=[],
                escalated_to=target,
                model_version=model_version,
                confidence=confidence,
                latency_ms=latency_ms,
                sources_used=[],
            )
        )

    @staticmethod
    def _hash_query(query: str) -> str:
        return f"sha256:{hashlib.sha256(query.encode('utf-8')).hexdigest()}"
