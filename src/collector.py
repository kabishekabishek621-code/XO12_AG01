from pathlib import Path

def load_failure_log(log_path: str) -> str:
    path = Path(log_path)
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")
    return path.read_text(encoding="utf-8", errors="ignore")

def load_code_diff(diff_path: str) -> str:
    path = Path(diff_path)
    if not path.exists():
        raise FileNotFoundError(f"Diff file not found: {diff_path}")
    return path.read_text(encoding="utf-8", errors="ignore")

def collect(log_path: str, diff_path: str) -> dict:
    logs = load_failure_log(log_path)
    diff = load_code_diff(diff_path)
    return {
        "logs": logs,
        "diff": diff,
        "log_length": len(logs),
        "diff_length": len(diff)
    }
