#!/usr/bin/env python3

import os
import re
import subprocess
from typing import List, Optional, Sequence


PUBLICATION_REVIEW_RE = re.compile(r"^publication-review-\d{4}-\d{2}-\d{2}\.md$")
PUBLICATION_REVIEW_DIR = os.path.join("docs")
PR_CHECKLIST = os.path.join("docs", "pr-prep-checklist.md")
REVIEW_GATES = os.path.join("docs", "REVIEW_GATES.md")


def run_cmd(args: Sequence[str]) -> Optional[str]:
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
    except Exception:
        return None
    return result.stdout.strip()


def find_latest_publication_review() -> Optional[str]:
    if not os.path.exists(PUBLICATION_REVIEW_DIR):
        return None

    files = sorted(
        [
            name
            for name in os.listdir(PUBLICATION_REVIEW_DIR)
            if PUBLICATION_REVIEW_RE.match(name)
        ],
        reverse=True,
    )
    if not files:
        return None
    return os.path.join(PUBLICATION_REVIEW_DIR, files[0])


def get_changed_files() -> List[str]:
    changed: set[str] = set()
    commands = [
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    for command in commands:
        output = run_cmd(command)
        if not output:
            continue
        changed.update(line.strip() for line in output.splitlines() if line.strip())
    return sorted(changed)


def load_text(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r") as f:
        return f.read()


def classify_review_coverage(review_text: str, changed_files: Sequence[str]) -> List[str]:
    missing = []
    for path in changed_files:
        if path.startswith("docs/") or path.startswith("scripts/"):
            if path not in review_text and f"`{path}`" not in review_text:
                missing.append(path)
    return missing


def main() -> int:
    print("=== REVIEW GATE CHECK ===\n")

    changed_files = get_changed_files()
    review_doc = find_latest_publication_review()
    review_text = load_text(review_doc) if review_doc else ""

    notes = []

    if os.path.exists(REVIEW_GATES):
        print(f"Review gates doc: {REVIEW_GATES}")
    else:
        notes.append("Missing docs/REVIEW_GATES.md")

    if os.path.exists(PR_CHECKLIST):
        print(f"PR checklist: {PR_CHECKLIST}")
    else:
        notes.append("Missing docs/pr-prep-checklist.md")

    if review_doc:
        print(f"Latest publication review: {review_doc}")
    else:
        notes.append("No publication review file found in docs/")

    print(f"Changed files in current diff: {len(changed_files)}")

    uncovered = classify_review_coverage(review_text, changed_files)
    if uncovered:
        notes.append("Changed docs/scripts missing from publication review:")
        notes.extend([f"  - {path}" for path in uncovered])

    print("\nRequired gates:")
    print("- Code review complete")
    print("- QC / validation complete")
    print("- Governance / legal / privacy review complete")

    if notes:
        print("\nWarnings:")
        for note in notes:
            print(f"- {note}")
        return 1

    print("\nNo missing review artifacts detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
