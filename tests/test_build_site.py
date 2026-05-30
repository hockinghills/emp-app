import importlib.util
import sys
from pathlib import Path

_BUILD_SITE = Path(__file__).resolve().parent.parent / "scripts" / "build_site.py"
_spec = importlib.util.spec_from_file_location("build_site", _BUILD_SITE)
build_site = importlib.util.module_from_spec(_spec)
sys.modules["build_site"] = build_site
_spec.loader.exec_module(build_site)

FORM_ENDPOINT = build_site.FORM_ENDPOINT
QUESTION = build_site.QUESTION
SITE_BASE = build_site.SITE_BASE
render_landing = build_site.render_landing
render_thanks = build_site.render_thanks


def test_landing_includes_sharpened_question():
    html_doc = render_landing("abc1234def", "2026-05-30T00:00:00+00:00", "0.0.1")
    assert "7 days" in html_doc
    assert "coordination breakdown" in html_doc
    assert QUESTION in html_doc.replace("&#x27;", "'")


def test_landing_has_form_field_and_optional_email():
    html_doc = render_landing("abc", "t", "v")
    assert 'name="story"' in html_doc
    assert "required" in html_doc
    assert 'name="email"' in html_doc
    assert "required " not in html_doc.split('name="email"', 1)[1].split(">", 1)[0]


def test_landing_posts_to_form_sink_and_redirects_to_thanks():
    html_doc = render_landing("abc", "t", "v")
    assert f'action="{FORM_ENDPOINT}"' in html_doc
    assert f"{SITE_BASE}/thanks.html" in html_doc


def test_landing_bakes_commit_for_verification():
    html_doc = render_landing("deadbeefcafe1234", "2026-05-30T00:00:00+00:00", "0.0.1")
    assert "deadbee" in html_doc
    assert "deadbeefcafe1234" in html_doc


def test_thanks_has_no_upsell():
    html_doc = render_thanks("abc", "t", "v")
    assert "Thank you" in html_doc
    assert "no upsell" in html_doc.lower()
    assert "<form" not in html_doc
