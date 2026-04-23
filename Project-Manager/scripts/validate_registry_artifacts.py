#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "config" / "registry-artifact-policy.json"
OUT_DIR = ROOT / "docs" / "session-artifacts" / "governance"


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True)


def tracked(repo: Path, rel: str) -> bool:
    cp = run_git(["ls-files", "--error-unmatch", rel], repo)
    return cp.returncode == 0


def ignored(repo: Path, rel: str) -> bool:
    cp = run_git(["check-ignore", rel], repo)
    return cp.returncode == 0


def main() -> int:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    default_required = policy.get("required_files", [])
    default_mode = policy.get("default_mode", "commit")
    targets = policy.get("targets", {})

    stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = OUT_DIR / f"REGISTRY_TARGET_VALIDATION-{stamp}.md"

    lines = [f"# Registry Target Validation ({stamp})", ""]
    failures = 0

    for name, cfg in targets.items():
        repo = ROOT / cfg["path"]
        mode = cfg.get("mode", default_mode)
        required = cfg.get("required_files", default_required)
        lines.extend([f"## {name}", "", f"- mode: `{mode}`"])

        for rel in required:
            path = repo / rel
            exists = path.exists()
            is_tracked = tracked(repo, rel)
            is_ignored = ignored(repo, rel)
            lines.append(
                f"- `{rel}`: exists={str(exists).lower()} tracked={str(is_tracked).lower()} ignored={str(is_ignored).lower()}"
            )

            if mode == "commit":
                if not exists or not is_tracked:
                    failures += 1
            elif mode == "ignore":
                if not is_ignored:
                    failures += 1
            else:
                failures += 1
        lines.append("")

    result = "PASS" if failures == 0 else "FAIL"
    lines.append(f"Result: **{result}**")
    lines.append(f"- validation_failures: {failures}")

    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {report.relative_to(ROOT)}")
    print(f"Result: {result}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
