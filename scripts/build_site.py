"""Build the deployable static site under _site/.

Renders the EMP-7 landing page: one question, one required answer, one
optional email, and a confirmation page. Commit SHA + build timestamp
are baked in so we can verify the deployed build matches HEAD.
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

QUESTION = (
    "In the last 7 days, what's the most painful coordination breakdown "
    "you hit with your team — a missed handoff, a forgotten decision, "
    "or duplicated work?"
)

FORM_ENDPOINT = "https://formsubmit.co/willie.stonehengeweb@gmail.com"
COUNTER_BEACON = "https://api.counterapi.dev/v1/emp-app/landing/up"
SITE_BASE = "https://hockinghills.github.io/emp-app"


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


_STYLE = (
    "body{font:16px/1.55 system-ui,-apple-system,sans-serif;"
    "max-width:36rem;margin:4rem auto;padding:0 1.25rem;color:#111;"
    "background:#fafafa}"
    "h1{font-size:1.5rem;line-height:1.35;margin:0 0 1.25rem;font-weight:600}"
    "p{margin:0 0 1rem;color:#333}"
    "label{display:block;font-weight:600;margin:1.25rem 0 .35rem;font-size:.95rem}"
    ".hint{font-weight:400;color:#666;font-size:.85rem;margin-left:.25rem}"
    "textarea,input[type=email]{width:100%;box-sizing:border-box;"
    "padding:.7rem .8rem;font:inherit;color:#111;background:#fff;"
    "border:1px solid #d4d4d8;border-radius:.4rem}"
    "textarea{min-height:7rem;resize:vertical}"
    "textarea:focus,input[type=email]:focus{outline:2px solid #2563eb;"
    "outline-offset:1px;border-color:#2563eb}"
    "button{margin-top:1.5rem;padding:.7rem 1.2rem;font:inherit;"
    "font-weight:600;color:#fff;background:#111;border:0;"
    "border-radius:.4rem;cursor:pointer}"
    "button:hover{background:#000}"
    "footer{margin-top:3rem;font-size:.75rem;color:#888}"
    "footer code{background:#f0f0f0;padding:.05rem .3rem;border-radius:.2rem}"
)


def render_landing(sha: str, build_time: str, version: str) -> str:
    short = _commit_short(sha)
    q = html.escape(QUESTION)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        "  <title>One question for founders</title>\n"
        '  <meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '  <meta name="description" content="One question. One answer. No upsell.">\n'
        f"  <style>{_STYLE}</style>\n"
        "</head>\n"
        "<body>\n"
        f"  <h1>{q}</h1>\n"
        "  <p>One question. One answer. No upsell. Two minutes.</p>\n"
        f'  <form action="{FORM_ENDPOINT}" method="POST">\n'
        '    <input type="hidden" name="_subject" value="EMP landing — new response">\n'
        '    <input type="hidden" name="_captcha" value="false">\n'
        f'    <input type="hidden" name="_next" value="{SITE_BASE}/thanks.html">\n'
        '    <input type="hidden" name="_template" value="table">\n'
        '    <input type="text" name="_honey" style="display:none"\n'
        '      tabindex="-1" autocomplete="off">\n'
        '    <label for="story">Your answer\n'
        '      <span class="hint">— concrete is better than tidy</span>\n'
        "    </label>\n"
        '    <textarea id="story" name="story" required placeholder="What\n'
        '      happened, who was involved, and what did it cost you?"></textarea>\n'
        '    <label for="email">Email\n'
        '      <span class="hint">— optional, only if you want a follow-up</span>\n'
        "    </label>\n"
        '    <input id="email" name="email" type="email"\n'
        '      autocomplete="email" placeholder="you@startup.com">\n'
        '    <button type="submit">Send</button>\n'
        "  </form>\n"
        "  <footer>\n"
        f"    Build <code>{html.escape(short)}</code> "
        f"(<code>{html.escape(sha)}</code>) · "
        f"<code>{html.escape(build_time)}</code> UTC · "
        f"v<code>{html.escape(version)}</code>\n"
        "  </footer>\n"
        f'  <script>fetch("{COUNTER_BEACON}",{{mode:"no-cors"}}).catch(()=>{{}});</script>\n'
        "</body>\n"
        "</html>\n"
    )


def render_thanks(sha: str, build_time: str, version: str) -> str:
    short = _commit_short(sha)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        "  <title>Thanks</title>\n"
        '  <meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f"  <style>{_STYLE}</style>\n"
        "</head>\n"
        "<body>\n"
        "  <h1>Got it. Thank you.</h1>\n"
        "  <p>That's the whole thing — no follow-up sequence, no upsell.</p>\n"
        "  <p>If you left an email, we may reach out once with a single\n"
        "    clarifying question. That's it.</p>\n"
        "  <footer>\n"
        f"    Build <code>{html.escape(short)}</code> · "
        f"<code>{html.escape(build_time)}</code> UTC · "
        f"v<code>{html.escape(version)}</code>\n"
        "  </footer>\n"
        "</body>\n"
        "</html>\n"
    )


def main() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sha = _commit_sha()
    build_time = _build_time()
    version = _app_version()
    landing = OUT_DIR / "index.html"
    thanks = OUT_DIR / "thanks.html"
    landing.write_text(render_landing(sha, build_time, version), encoding="utf-8")
    thanks.write_text(render_thanks(sha, build_time, version), encoding="utf-8")
    print(f"wrote {landing} and {thanks} (commit={_commit_short(sha)})")
    return landing


if __name__ == "__main__":
    main()
