# ============================================================
# Dockerfile for the portfolio site.
#
# A Dockerfile is a RECIPE: each instruction adds a layer to the
# image. Docker caches layers, so the ORDER matters — put the
# things that change least often (dependencies) BEFORE the things
# that change most often (your code). That way editing app.py
# doesn't re-download Flask on every build.
# ============================================================

# Base image: official Python, "slim" variant = Debian minus the bloat.
# (Spec decision: python:3.12-slim.)
FROM python:3.12-slim

# All following commands run relative to this directory inside the image.
# It's created automatically if it doesn't exist.
WORKDIR /app

# 1) Copy ONLY the requirements file first...
COPY requirements.txt .

# 2) ...and install dependencies. This layer is cached until
#    requirements.txt changes. --no-cache-dir keeps the image smaller
#    (pip's download cache is useless inside an immutable image).
RUN pip install --no-cache-dir -r requirements.txt

# 3) NOW copy the rest of the code. Editing app.py only invalidates
#    the layers from here down — the pip install above stays cached.
COPY . .

# Documentation for humans and tools: "this app listens on 8000".
# NOTE: EXPOSE does NOT publish the port — you still need -p 8000:8000.
EXPOSE 8000

# The command the container runs when it starts.
# "exec form" (JSON array) = no shell wrapper, so Ctrl+C / docker stop
# signals reach Python directly and the container shuts down cleanly.
CMD ["python", "app.py"]

# Build:  docker build -t <dockerhub-user>/portfolio:latest .
# Run:    docker run -p 8000:8000 <dockerhub-user>/portfolio:latest
# Visit:  http://localhost:8000
