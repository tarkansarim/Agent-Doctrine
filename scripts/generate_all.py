from __future__ import annotations

from doctrine_common import provider_names, write_generated


def main() -> int:
    for provider in provider_names():
        path = write_generated(provider)
        print(f"generated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
