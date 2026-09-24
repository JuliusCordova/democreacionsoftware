"""Generate reproducible local/Cloud Shell evidence for Sprint 0."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "docs" / "evidence" / "generated"


def run(name: str, command: list[str]) -> dict:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "name": name,
        "status": "PASS" if completed.returncode == 0 else "FAIL",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def main() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = OUT_ROOT / stamp
    out.mkdir(parents=True, exist_ok=False)

    checks = [
        run("unit_tests", ["python3", "-m", "pytest", "-q"]),
        run("compile", ["python3", "-m", "compileall", "-q", "src", "tests", "scripts"]),
        run("smoke", ["python3", "-m", "stock_unico.smoke"]),
    ]

    metadata = {
        "timestamp_utc": stamp,
        "git_sha": git("rev-parse", "HEAD"),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "checks": {item["name"]: item["status"] for item in checks},
    }

    (out / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )

    for item in checks:
        (out / f"{item['name']}.json").write_text(
            json.dumps(item, indent=2) + "\n", encoding="utf-8"
        )

    lines = [
        "# Cloud Shell Evidence",
        "",
        f"- Timestamp UTC: `{metadata['timestamp_utc']}`",
        f"- Git SHA: `{metadata['git_sha']}`",
        f"- Branch: `{metadata['branch']}`",
        "",
        "## Checks",
        "",
    ]
    for item in checks:
        lines.append(f"- **{item['status']}** — {item['name']}")

    (out / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(out.relative_to(ROOT))
    return 0 if all(item["status"] == "PASS" for item in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
