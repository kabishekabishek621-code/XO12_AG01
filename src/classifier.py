from typing import Dict, List
import re

def extract_evidence(logs: str, diff: str) -> Dict:
    logs_lower = logs.lower()
    diff_lower = diff.lower()

    # Check if diff has actual code changes (not just comments or empty)
    code_lines_added = 0
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            clean = line[1:].strip()
            # Ignore comment-only lines and empty lines
            if clean and not clean.startswith("#") and not clean.startswith("//"):
                code_lines_added += 1

    return {
        "has_stack_trace": "traceback" in logs_lower or "error:" in logs_lower or "assertionerror" in logs_lower,
        "mentions_network": any(word in logs_lower for word in ["timeout", "connection", "network", "dns", "unreachable"]),
        "mentions_secret": any(word in logs_lower for word in ["secret", "token", "unauthorized", "permission denied", "access denied"]),
        "mentions_flaky_words": any(word in logs_lower for word in ["flaky", "intermittent", "sometimes", "occasionally"]),
        "diff_touches_test": "test" in diff_lower or "spec" in diff_lower,
        "has_real_code_change": code_lines_added > 0,
        "diff_is_empty": len(diff.strip()) < 20,
    }

def classify(logs: str, diff: str) -> Dict:
    evidence = extract_evidence(logs, diff)
    reasons: List[str] = []

    # 1. Environment Issue (highest priority)
    if evidence["mentions_network"] or evidence["mentions_secret"]:
        reasons.append("Found environment / infrastructure related error in logs")
        return {
            "classification": "Environment Issue",
            "confidence": 0.82,
            "evidence": evidence,
            "reasons": reasons,
            "action": "Do not retry code. Check secrets, network or runner."
        }

    # 2. Flaky Test
    if evidence["mentions_flaky_words"] or (
        evidence["has_stack_trace"] and not evidence["has_real_code_change"]
    ):
        reasons.append("No real code change found or flaky signals detected")
        return {
            "classification": "Flaky Test",
            "confidence": 0.78,
            "evidence": evidence,
            "reasons": reasons,
            "action": "Retry recommended (max 2 times) then re-evaluate"
        }

    # 3. Genuine Regression
    if evidence["has_stack_trace"] and evidence["has_real_code_change"] and evidence["diff_touches_test"]:
        reasons.append("Stack trace present and real code change found in test-related file")
        return {
            "classification": "Genuine Regression",
            "confidence": 0.85,
            "evidence": evidence,
            "reasons": reasons,
            "action": "Escalate to developer. Do not auto-retry."
        }

    # 4. Unclear
    reasons.append("Not enough clear evidence to decide confidently")
    return {
        "classification": "Unclear",
        "confidence": 0.45,
        "evidence": evidence,
        "reasons": reasons,
        "action": "Escalate with summary for human review"
    }
