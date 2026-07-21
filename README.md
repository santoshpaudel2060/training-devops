# My Portfolio 🧑‍💻

A personal portfolio site served by a tiny **Flask** app — the star of your
bootcamp week. On Day 2 it gets CI, on Day 3 it gets a container, on Day 4 it
gets deployed to a cloud VM with Terraform.

## What's inside

```
portfolio-python/
├── app.py                    ← Flask app (/, /health), port 8000
├── templates/index.html      ← the portfolio page (Jinja2 template)
├── static/css/style.css      ← styling (self-contained, no CDNs)
├── static/js/main.js         ← scroll reveals + animated skill bars
├── requirements.txt          ← Python dependencies (just Flask)
├── tests/test_smoke.py       ← smoke tests used by CI
├── Dockerfile                ← recipe to containerize the app
└── .github/workflows/ci.yml  ← GitHub Actions pipeline
```

## Run it locally (no Docker)

```bash
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
$ python app.py
```

Open **http://localhost:8000** — you should see Alex Devlin's portfolio.
Check **http://localhost:8000/health** — you should get:

```json
{"service": "portfolio", "status": "ok"}
```

Run the tests the same way CI does:

```bash
$ pip install pytest flake8
$ flake8 . --max-line-length 100
$ pytest -v
```

## Run it with Docker 🐳

```bash
# Build the image (the dot = "use the Dockerfile in this folder")
$ docker build -t <dockerhub-user>/portfolio:latest .

# Run it, mapping YOUR port 8000 → the CONTAINER's port 8000
$ docker run -p 8000:8000 <dockerhub-user>/portfolio:latest
```

Same URL: **http://localhost:8000**. Try to break it: stop the container
(`Ctrl+C`), run it again, and watch the footer's visit counter reset —
container memory is disposable. That's why real state lives in databases.

## How the CI works ⚙️

Every `git push` (and every pull request) triggers
`.github/workflows/ci.yml` on a fresh GitHub-hosted Ubuntu VM:

1. **Checkout** — clones your code onto the VM.
2. **Setup Python 3.12** — same version as local dev and the Docker image.
3. **Install** — `pip install -r requirements.txt flake8 pytest`.
4. **Lint** — `flake8` catches typos and style slips before a human ever
   reviews the code.
5. **Test** — `pytest` runs `tests/test_smoke.py`: `/` must return 200,
   `/health` must return `{"status": "ok"}`.

Green ✅ = safe to merge. Red ❌ = click the failed step and read the log —
the answer is almost always in the last 20 lines.

There's a second job, `build-and-push`, **commented out until Day 3**. Once
you have Docker Hub secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`) set in
*Repo → Settings → Secrets and variables → Actions*, uncomment it and every
push to `main` will automatically build the image and publish it as
`<dockerhub-user>/portfolio:latest` **and** `:<commit-sha>` — that's
Continuous Delivery of your very own portfolio.
