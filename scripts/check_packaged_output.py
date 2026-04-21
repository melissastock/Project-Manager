#!/usr/bin/env python3

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PACKAGE_FILES = [
    "docs/delivery/release-package.md",
    "docs/delivery/release-notes.md",
    "docs/delivery/rollback-plan.md",
    "docs/delivery/output-acceptance.md",
]

REQUIRED_RELEASE_PACKAGE_MARKERS = [
    "package version",
    "owner",
    "audience",
    "included artifacts",
    "distribution channel",
]

REQUIRED_ACCEPTANCE_MARKERS = [
    "accepted by",
    "acceptance date",
    "accepted scope",
    "residual risks",
]


def load(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def contains_all_markers(text: str, markers: list[str]) -> bool:
    lowered = text.lower()
    return all(marker in lowered for marker in markers)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate packaged-output artifacts before release."
    )
    parser.add_argument("--target", required=True, help="Target project path to validate.")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = ROOT / target

    failures: list[str] = []

    for rel in REQUIRED_PACKAGE_FILES:
        if not (target / rel).exists():
            failures.append(f"Missing required packaging file: {rel}")

    release_package = load(target / "docs/delivery/release-package.md")
    output_acceptance = load(target / "docs/delivery/output-acceptance.md")

    if release_package and not contains_all_markers(
        release_package, REQUIRED_RELEASE_PACKAGE_MARKERS
    ):
        failures.append(
            "release-package.md is missing one or more required fields "
            "(package version, owner, audience, included artifacts, distribution channel)."
        )

    if output_acceptance and not contains_all_markers(
        output_acceptance, REQUIRED_ACCEPTANCE_MARKERS
    ):
        failures.append(
            "output-acceptance.md is missing one or more acceptance fields "
            "(accepted by, acceptance date, accepted scope, residual risks)."
        )

    if failures:
        print("Packaged output gate: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Packaged output gate: PASS")
    print("Release packaging and acceptance artifacts are present and complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
