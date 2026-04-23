from __future__ import annotations

import sys
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from project_config import set_project_config  # noqa: E402


with tempfile.TemporaryDirectory() as temp:
    project_path = Path(temp) / "demo-project"

    dry_run = set_project_config(project_path, {"trust_level": "trusted"}, dry_run=True)
    print(dry_run["config_path"])
    print(dry_run["diff"])

    applied = set_project_config(project_path, {"trust_level": "trusted"}, apply=True)
    print(applied["success"])
    print((project_path / ".tooling" / "config.toml").read_text(encoding="utf-8"))
