from __future__ import annotations

from .models import ReadinessDimensionScore, SignalSnapshot


def readiness_band(score: int, bands: list[dict]) -> str:
    for band in sorted(bands, key=lambda b: int(b["min_score"]), reverse=True):
        if score >= int(band["min_score"]):
            return str(band["label"])
    return "critical"


def compute_base_score(snapshot: SignalSnapshot, project: dict, policy: dict) -> int:
    score = 50
    score += int(policy["priority_weights"].get(project.get("priority_class", ""), 0))
    score += int(policy["lane_weights"].get(project.get("lane", ""), 0))
    penalties = policy["risk_penalties"]

    if not snapshot.is_git_repo:
        # Repo can be fully onboarded in config while this runtime cannot access nested git metadata.
        # Keep this visible but avoid mislabeling onboarding as failed.
        missing_penalty = int(penalties["missing_git_repo"])
        if project.get("intake_stage"):
            missing_penalty = max(5, missing_penalty // 3)
        score -= missing_penalty
    score -= snapshot.staged_count * int(penalties["staged"])
    score -= snapshot.unstaged_count * int(penalties["unstaged"])
    score -= min(snapshot.untracked_count * int(penalties["untracked_per_item"]), int(penalties["max_untracked_penalty"]))
    if snapshot.behind and snapshot.behind > 0:
        score -= snapshot.behind * int(penalties["behind_per_commit"])

    return max(0, min(100, score))


def compute_dimensions(base_score: int, snapshot: SignalSnapshot, policy: dict) -> list[ReadinessDimensionScore]:
    w = policy["dimension_weights"]
    dims = []
    for key in [
        "operations",
        "legal_compliance",
        "marketing",
        "analysis_reporting",
        "development",
        "financial",
        "investor_readiness",
    ]:
        score = base_score
        evidence = []
        if key == "operations":
            evidence.append(f"drift staged={snapshot.staged_count}, unstaged={snapshot.unstaged_count}, untracked={snapshot.untracked_count}")
            if snapshot.untracked_count > 0:
                score -= 10
        elif key == "development":
            evidence.append(f"branch {snapshot.branch}, ahead={snapshot.ahead}, behind={snapshot.behind}")
            if snapshot.behind and snapshot.behind > 0:
                score -= 8
        elif key in {"analysis_reporting", "financial"}:
            evidence.append(f"backlog docs={len(snapshot.backlog_files)}, sprint docs={len(snapshot.sprint_files)}")
            if not snapshot.backlog_files:
                score -= 7
        elif key == "legal_compliance":
            evidence.append("Derived from repository governance and traceability signals")
        elif key == "investor_readiness":
            evidence.append("Uses delivery discipline and reporting health proxy signals")
        else:
            evidence.append("Derived from git workflow stability indicators")

        weighted = int(round(max(0, min(100, score)) * float(w.get(key, 0.1))))
        # Convert weighted contribution back to 0-100 display to keep cards intuitive.
        display = int(round(weighted / float(w.get(key, 0.1)))) if float(w.get(key, 0.1)) > 0 else max(0, min(100, score))
        dims.append(ReadinessDimensionScore(dimension=key, score=max(0, min(100, display)), evidence=evidence))
    return dims
