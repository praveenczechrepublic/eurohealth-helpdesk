"""
EuroHealth AI Helpdesk — Structured Audit Logger
=================================================
Writes schema-aligned JSON Lines audit records to local storage.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from threading import Lock


class AuditLogValidationError(ValueError):
    pass


@dataclass
class AuditLogger:
    log_path: Path = Path("data/audit/audit-events.jsonl")
    schema_path: Path = Path("governance/evidence/audit-log-schema.json")

    def __post_init__(self) -> None:
        self._lock = Lock()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._schema = self._load_schema()

    def _load_schema(self) -> dict:
        with self.schema_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def write_event(self, event: dict) -> None:
        self._validate(event)
        payload = json.dumps(event, sort_keys=True, ensure_ascii=False)
        with self._lock:
            with self.log_path.open("a", encoding="utf-8") as fh:
                fh.write(payload + "\n")

    def _validate(self, event: dict) -> None:
        required = self._schema.get("required", [])
        missing = [field for field in required if field not in event]
        if missing:
            raise AuditLogValidationError(f"Missing required fields: {missing}")

        # Enforce required nested latency keys from the schema subset we rely on.
        latency = event.get("latency_ms")
        if not isinstance(latency, dict):
            raise AuditLogValidationError("latency_ms must be an object")
        for field in ("policy_evaluation", "total"):
            if field not in latency:
                raise AuditLogValidationError(f"latency_ms missing required field: {field}")

        if self._schema.get("additionalProperties") is False:
            allowed = set(self._schema.get("properties", {}).keys())
            unknown = [key for key in event.keys() if key not in allowed]
            if unknown:
                raise AuditLogValidationError(f"Unexpected fields: {unknown}")
