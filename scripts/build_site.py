"""Build the deployable static site under _site/.

Reads commit SHA + build timestamp from the environment (with git fallbacks)
and writes a single index.html that proves which commit is live.
"""

from __future__ import annotations

import datetime as _dt
import html
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "_site"


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=ROOT, text=True).strip()
    except Exception:
        return ""


def _commit_sha() -> str:
    return os.environ.get("GITHUB_SHA") or _run(["git", "rev-parse", "HEAD"]) or "unknown"


def _commit_short(sha: str) -> str:
    return sha[:7] if sha and sha != "unknown" else "unknown"


def _build_time() -> str:
    return _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds")


def _app_version() -> str:
    sys.path.insert(0, str(ROOT / "src"))
    try:
        from app import __version__
    except Exception:
        return "unknown"
    return __version__


def render(sha: str, build_time: str, version: str) -> str:
    short = _commit_short(sha)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        "  <title>app — hello</title>\n"
        '  <meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "  <style>"
        "body{font:14px/1.5 system-ui,sans-serif;max-width:42rem;"
        "margin:3rem auto;padding:0 1rem;color:#111}"
        "code{background:#f4f4f5;padding:.1rem .3rem;border-radius:.2rem}"
        "dt{font-weight:600;margin-top:.6rem}"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        "  <h1>Hello, world.</h1>\n"
        "  <p>This page is the smallest deployable artifact for <code>app</code>.</p>\n"
        "  <dl>\n"
        f"    <dt>Version</dt><dd><code>{html.escape(version)}</code></dd>\n"
        f"    <dt>Commit</dt><dd><code>{html.escape(short)}</code> "
        f"(<code>{html.escape(sha)}</code>)</dd>\n"
        f"    <dt>Built</dt><dd><code>{html.escape(build_time)}</code> UTC</dd>\n"
        "  </dl>\n"
        "</body>\n"
        "</html>\n"
    )


def main() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sha = _commit_sha()
    html_doc = render(sha=sha, build_time=_build_time(), version=_app_version())
    out_file = OUT_DIR / "index.html"
    out_file.write_text(html_doc, encoding="utf-8")
    print(f"wrote {out_file} (commit={_commit_short(sha)})")
    return out_file


if __name__ == "__main__":
    main()
