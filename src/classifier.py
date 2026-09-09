from typing import Dict, List

def extract_evidence(logs: str, diff: str) -> Dict:
    logs_lower = logs.lower()
    diff_lower = diff.lower()

    return {
        "has_stack_trace": "traceback" in logs_lower or "error:" in logs_lower,
        "mentions_network": any(word in logs_lower for word in ["timeout", "connection", "network", "dns"]),
        "mentions_secret": any(word in logs_lower for word in ["secret", "token", "unauthorized", "permission denied"]),
        "mentions_flaky_words": any(word in logs_lower for word in ["flaky", "intermittent", "sometimes"]),
        "diff_touches_test": "test" in diff_lower or "spec" in diff_lower,
        "diff_is_empty": len(diff.strip()) < 20,
    }

def classify(logs: str, diff: str) -> Dict:
    evidence = extract_evidence(logs, diff)
    reasons: List[str] = []

    if evidence["mentions_network"] or evidence["mentions_secret"]:
        reasons.append("Found environment-related error in logs")
        return {
            "classification": "Environment Issue",
            "confidence": 0.75,
            "evidence": evidence,
            "reasons": reasons,
            "action": "Do not retry code. Check infrastructure / secrets."
        }

    if evidence["mentions_flaky_words"] or (evidence["has_stack_trace"] and not evidence["diff_touches_test"]):
        reasons.append("Possible flaky behaviour or no related code change")
        return {
            "classification": "Flaky Test",
            "confidence": 0.65,
            "evidence": evidence,
            "reasons": reasons,
            "action": "Retry (max 2 times) then re-evaluate"
        }

    if evidence["has_stack_trace"] and evidence["diff_touches_test"]:
        reasons.append("Stack trace present and diff touches test code")
        return {
            "classification": "Genuine Regression",
            "confidence": 0.80,
            "evidence": evidence,
            "reasons": reasons,
            "action": "Escalate to developer. Do not auto-retry."
        }

    reasons.append("Not enough clear evidence")
    return {
        "classification": "Unclear",
        "confidence": 0.40,
        "evidence": evidence,
        "reasons": reasons,
        "action": "Escalate with summary"
    }
