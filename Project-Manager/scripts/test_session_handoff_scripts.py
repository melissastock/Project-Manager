import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import create_session_handoff
from scripts import session_handoff_common


class SessionHandoffScriptTests(unittest.TestCase):
    def test_normalize_project_name(self) -> None:
        self.assertEqual(
            create_session_handoff.normalize_project_name(" Project Manager / Alpha "),
            "project-manager-alpha",
        )

    def test_build_handoff_filename_matches_expected_pattern(self) -> None:
        filename = create_session_handoff.build_handoff_filename("project-manager")
        self.assertRegex(filename, r"^\d{4}-\d{2}-\d{2}-project-manager-handoff\.md$")

    def test_find_latest_handoff_ignores_readme(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            handoff_dir = Path(tmpdir)
            (handoff_dir / "README.md").write_text("# Session Handoffs\n")
            (handoff_dir / "2026-04-01-project-manager-handoff.md").write_text(
                "# Developer Session Handoff\n\n# PM-Ready Summary (Read This First)\n- older\n---\n"
            )
            (handoff_dir / "2026-04-02-project-manager-handoff.md").write_text(
                "# Developer Session Handoff\n\n# PM-Ready Summary (Read This First)\n- newer\n---\n"
            )

            latest = session_handoff_common.find_latest_handoff(str(handoff_dir))

            self.assertEqual(
                latest,
                str(handoff_dir / "2026-04-02-project-manager-handoff.md"),
            )

    def test_read_summary_extracts_pm_ready_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            handoff = Path(tmpdir) / "2026-04-02-project-manager-handoff.md"
            handoff.write_text(
                "# Developer Session Handoff\n\n"
                "# PM-Ready Summary (Read This First)\n"
                "## What Changed (Facts Only)\n"
                "- updated scripts\n"
                "---\n"
                "## Evidence Log\n"
            )

            summary = session_handoff_common.read_summary(str(handoff))

            self.assertIn("## What Changed (Facts Only)", summary)
            self.assertIn("- updated scripts", summary)
            self.assertNotIn("## Evidence Log", summary)

    def test_create_session_handoff_main_creates_expected_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(create_session_handoff, "HANDOFF_DIR", tmpdir):
                with patch("builtins.input", return_value="Project Manager"):
                    result = create_session_handoff.main()

            self.assertEqual(result, 0)
            created_files = list(Path(tmpdir).glob("*-project-manager-handoff.md"))
            self.assertEqual(len(created_files), 1)
            self.assertIn("Developer Session Handoff", created_files[0].read_text())


if __name__ == "__main__":
    unittest.main()
