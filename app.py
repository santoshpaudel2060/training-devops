"""
My Portfolio — a tiny Flask app that serves a personal portfolio site.

WHY Flask and not just plain HTML files?
----------------------------------------
A static site would work, but wrapping it in a tiny Python web server gives us:
  1. A real "app" to containerize on Day 3 (Dockerfile, ports, CMD...).
  2. A /health endpoint that CI, Docker, and (later) Kubernetes can probe.
  3. A little dynamic behavior (current year, visit counter) so you can SEE
     that a server is doing work on every request.

Run it locally:   python app.py        → http://localhost:8000
Run it in Docker: docker run -p 8000:8000 <dockerhub-user>/portfolio:latest
"""

from datetime import datetime, timezone

from flask import Flask, jsonify, render_template

# Flask automatically serves files from ./static at /static/... and looks for
# HTML templates in ./templates — that's why the folders are named that way.
app = Flask(__name__)

# A super-simple in-memory visit counter.
# ⚠️ Teaching moment: this lives in the PROCESS memory. Restart the container
# and it resets to zero. That's why real apps keep state in a DATABASE
# (see the TaskForge project on Day 3!). Containers should be disposable.
visit_count = 0


@app.route("/")
def index():
    """Serve the portfolio page, injecting a bit of dynamic data."""
    global visit_count
    visit_count += 1
    return render_template(
        "index.html",
        year=datetime.now(timezone.utc).year,  # footer never goes stale
        visits=visit_count,                    # proof the server is alive
    )


@app.route("/health")
def health():
    """
    Health check endpoint.

    Returns a tiny JSON payload. CI smoke tests hit this, and later Docker
    HEALTHCHECKs / Kubernetes liveness probes can too. Convention: return
    HTTP 200 + {"status": "ok"} when the app is happy.
    """
    return jsonify(status="ok", service="portfolio")


if __name__ == "__main__":
    # host="0.0.0.0" is CRITICAL for Docker: it makes Flask listen on ALL
    # network interfaces, not just localhost *inside* the container.
    # If you bind to 127.0.0.1 in a container, port mapping won't work and
    # you'll stare at "connection reset" errors. Classic gotcha!
    app.run(host="0.0.0.0", port=8000)
