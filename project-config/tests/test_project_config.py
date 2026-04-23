from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from project_config import (  # noqa: E402
    read_project_config,
    set_project_config,
    update_project_table_text,
    validate_project_config,
)


class ProjectConfigTests(unittest.TestCase):
    def test_adds_missing_project_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "repo"
            result = set_project_config(project, {"trust_level": "trusted"}, apply=True)

            config_path = project / ".tooling" / "config.toml"
            self.assertTrue(result["success"])
            self.assertTrue(result["config_created"])
            self.assertEqual(result["changed_keys"], ["trust_level"])
            self.assertTrue(config_path.exists())
            self.assertIn('trust_level = "trusted"', config_path.read_text(encoding="utf-8"))
            self.assertTrue(validate_project_config(config_path=config_path)["ok"])

    def test_dry_run_returns_readable_unified_diff(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "repo"
            result = set_project_config(project, {"trust_level": "trusted"}, dry_run=True)

            self.assertTrue(result["success"])
            self.assertFalse((project / ".tooling" / "config.toml").exists())
            self.assertIn("\n+++ ", result["diff"])
            self.assertIn("@@ -0,0 +1,2 @@\n", result["diff"])

    def test_updates_existing_project_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "repo"
            config = project / ".tooling" / "config.toml"
            config.parent.mkdir(parents=True)
            config.write_text(
                "# keep me\n"
                f"[projects.'{project}']\n"
                'trust_level = "untrusted" # explain\n'
                "\n"
                "[unrelated]\n"
                'name = "stable"\n',
                encoding="utf-8",
            )

            result = set_project_config(project, {"trust_level": "trusted"}, apply=True)
            text = config.read_text(encoding="utf-8")

            self.assertTrue(result["success"])
            self.assertFalse(result["config_created"])
            self.assertIn("# keep me\n", text)
            self.assertIn('trust_level = "trusted" # explain', text)
            self.assertIn("[unrelated]\nname = \"stable\"\n", text)
            self.assertEqual(text.count("trust_level"), 1)
            self.assertIsNotNone(result["backup_path"])
            self.assertTrue(Path(result["backup_path"]).exists())

    def test_parent_trusted_child_can_keep_inheritance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp) / "parent"
            child = parent / "child"
            parent_config = parent / ".tooling" / "config.toml"
            parent_config.parent.mkdir(parents=True)
            parent_config.write_text(
                f"[projects.'{parent}']\n"
                'trust_level = "trusted"\n',
                encoding="utf-8",
            )

            result = set_project_config(
                child,
                {"trust_level": "trusted"},
                dry_run=True,
                inheritance_strategy="keep",
            )

            self.assertTrue(result["success"])
            self.assertFalse(result["changed"])
            self.assertEqual(result["changed_keys"], [])
            self.assertEqual(result["inheritance"][0]["relationship"], "parent")
            self.assertFalse((child / ".tooling" / "config.toml").exists())

    def test_windows_path_case_difference_matches_existing_key(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            config = Path(temp) / "config.toml"
            config.write_text(
                "[projects.'C:\\Users\\Charlie\\Repo']\n"
                'trust_level = "untrusted"\n',
                encoding="utf-8",
            )

            result = set_project_config(
                "c:\\users\\charlie\\repo",
                {"trust_level": "trusted"},
                apply=True,
                config_path=config,
            )
            text = config.read_text(encoding="utf-8")

            self.assertTrue(result["success"])
            self.assertEqual(text.count("[projects."), 1)
            self.assertIn("[projects.'C:\\Users\\Charlie\\Repo']", text)
            self.assertIn('trust_level = "trusted"', text)

    def test_repeated_apply_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "repo"
            first = set_project_config(project, {"trust_level": "trusted"}, apply=True)
            config = project / ".tooling" / "config.toml"
            before = config.read_text(encoding="utf-8")
            second = set_project_config(project, {"trust_level": "trusted"}, apply=True)
            after = config.read_text(encoding="utf-8")

            self.assertTrue(first["changed"])
            self.assertFalse(second["changed"])
            self.assertEqual(before, after)
            self.assertIsNone(second["backup_path"])

    def test_comments_and_unrelated_sections_stay_stable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "repo"
            before = (
                "# leading comment\n"
                "[alpha]\n"
                "value = 1\n"
                "\n"
                f"[projects.'{project}']\n"
                "# table comment\n"
                'trust_level = "untrusted"\n'
                "\n"
                "[omega]\n"
                "value = 2\n"
            )

            after, changed_keys, created = update_project_table_text(
                before,
                project,
                {"trust_level": "trusted"},
            )

            self.assertEqual(changed_keys, ["trust_level"])
            self.assertFalse(created)
            self.assertIn("# leading comment\n[alpha]\nvalue = 1\n", after)
            self.assertIn("# table comment\n", after)
            self.assertIn("[omega]\nvalue = 2\n", after)

    def test_read_reports_direct_and_effective_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "repo"
            config = project / ".tooling" / "config.toml"
            config.parent.mkdir(parents=True)
            config.write_text(
                f"[projects.'{project}']\n"
                'trust_level = "trusted"\n',
                encoding="utf-8",
            )

            result = read_project_config(project)

            self.assertEqual(result["direct"], {"trust_level": "trusted"})
            self.assertEqual(result["effective"]["trust_level"], "trusted")


if __name__ == "__main__":
    unittest.main()
