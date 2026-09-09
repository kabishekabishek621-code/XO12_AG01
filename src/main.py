from collector import collect
from classifier import classify
import json

def run_triage(log_path: str, diff_path: str) -> dict:
    data = collect(log_path, diff_path)
    result = classify(data["logs"], data["diff"])
    return {
        "classification": result["classification"],
        "confidence": result["confidence"],
        "reasons": result["reasons"],
        "action": result["action"],
        "evidence": result["evidence"]
    }

if __name__ == "__main__":
    try:
        result = run_triage("samples/failure.log", "samples/code.diff")
        print(json.dumps(result, indent=2))
    except FileNotFoundError as e:
        print("Sample files not found yet.")
        print(e)
