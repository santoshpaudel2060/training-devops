"""
Smoke tests — the bare minimum "is it plugged in?" checks.

They don't test business logic (there barely is any); they prove the app
boots and answers HTTP. That's exactly what you want CI to verify on every
push: "did I just break the site?"

Run locally:  pytest
(CI runs the same command — same tests locally and in the pipeline,
that's the whole point.)
"""

import sys
from pathlib import Path

# Make `import app` work no matter where pytest is launched from:
# add the project root (one level up from tests/) to Python's module path.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app  # noqa: E402  (import after sys.path tweak, on purpose)


def test_homepage_returns_200():
    """The portfolio page should load and actually contain our content."""
    # Flask's built-in test client fakes HTTP requests — no server,
    # no ports, no network. Fast and reliable in CI.
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Alex Devlin" in response.data


def test_health_returns_ok():
    """/health must return 200 + {"status": "ok"} — CI, Docker and k8s rely on it."""
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "ok"
