from __future__ import annotations

from doctrine_common import write_generated


def main() -> int:
    path = write_generated("codex")
    print(f"generated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
