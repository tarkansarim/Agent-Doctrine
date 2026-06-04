from __future__ import annotations

from pathlib import Path

from install_skill_common import main_for


if __name__ == "__main__":
    raise SystemExit(main_for("claude", Path.home() / ".claude" / "skills"))
