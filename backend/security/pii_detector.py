"""
PII detection and redaction — regex-based, no ML model required.
Detects common PII types before storage and before display.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class PIIResult:
    has_pii: bool
    pii_types: list[str]
    redacted_text: str
    matches: dict[str, list[str]]  # type → matched strings


class PIIDetector:
    """Detects and redacts PII from text using compiled regex patterns."""

    # Pattern registry: name → compiled regex
    _PATTERNS: dict[str, re.Pattern] = {
        "email":         re.compile(r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b'),
        "phone_us":      re.compile(r'\b(\+1[\s.\-]?)?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}\b'),
        "ssn":           re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        "credit_card":   re.compile(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b'),
        "ip_address":    re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
        "passport_us":   re.compile(r'\b[A-Z]{1,2}\d{6,9}\b'),
        "date_of_birth": re.compile(
            r'\b(?:DOB|Date\s+of\s+Birth|Born(?:\s+on)?)\s*[:\-]?\s*\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b',
            re.I,
        ),
        "bank_routing":  re.compile(r'\b0\d{8}\b'),  # 9-digit ABA routing starting with 0
        "iban":          re.compile(r'\b[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}[A-Z0-9]{0,16}\b'),
        "aws_key":       re.compile(r'\b(?:AKIA|AIPA|AIDA|AROA|ASCA|ASIA)[A-Z0-9]{16}\b'),
        "api_key_generic": re.compile(r'\b(?:api[_\-]?key|secret[_\-]?key|access[_\-]?token)\s*[=:]\s*[A-Za-z0-9_\-]{16,}\b', re.I),
    }

    @classmethod
    def detect(cls, text: str, types_to_check: list[str] | None = None) -> PIIResult:
        """
        Scan text for PII. Returns a PIIResult with types found and redacted version.
        If types_to_check is provided, only those PII types are scanned.
        """
        patterns = (
            {k: v for k, v in cls._PATTERNS.items() if k in types_to_check}
            if types_to_check
            else cls._PATTERNS
        )

        found_types: list[str] = []
        matches: dict[str, list[str]] = {}
        redacted = text

        for pii_type, pattern in patterns.items():
            found = pattern.findall(text)
            if found:
                found_types.append(pii_type)
                # findall may return tuples (for groups) — flatten
                matches[pii_type] = [m if isinstance(m, str) else m[0] for m in found]

        return PIIResult(
            has_pii=bool(found_types),
            pii_types=found_types,
            redacted_text=text,  # full redaction done in redact()
            matches=matches,
        )

    @classmethod
    def redact(cls, text: str, replacement: str = "[REDACTED]", types_to_redact: list[str] | None = None) -> str:
        """Replace all detected PII with the replacement string."""
        patterns = (
            {k: v for k, v in cls._PATTERNS.items() if k in types_to_redact}
            if types_to_redact
            else cls._PATTERNS
        )
        redacted = text
        for pattern in patterns.values():
            redacted = pattern.sub(replacement, redacted)
        return redacted

    @classmethod
    def is_safe_to_store(cls, text: str, allowed_pii_types: list[str] | None = None) -> bool:
        """
        Returns True if the text contains no PII (or only allowed PII types).
        Example: HR system may allow 'email' but not 'ssn' or 'credit_card'.
        """
        result = cls.detect(text)
        if not result.has_pii:
            return True
        if allowed_pii_types is None:
            return False
        # Safe if all found types are in the allowed list
        return all(t in allowed_pii_types for t in result.pii_types)

    @classmethod
    def get_pii_summary(cls, text: str) -> str:
        """Return a human-readable summary of detected PII types."""
        result = cls.detect(text)
        if not result.has_pii:
            return "No PII detected."
        return f"PII detected: {', '.join(result.pii_types)}"
