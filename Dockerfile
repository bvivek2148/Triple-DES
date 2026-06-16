# ── Build stage ──────────────────────────────────────────────────────────────
FROM python:3.11-slim AS base

# System dependencies for pycryptodome
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn python-dotenv

# Copy application source
COPY . .

# ── Create required runtime directories ──────────────────────────────────────
RUN mkdir -p uploads secure_keys database

# ── Runtime configuration ────────────────────────────────────────────────────
ENV FLASK_DEBUG=false
ENV PORT=8000

EXPOSE 8000

# Health-check so container orchestrators know the app is up
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# ── Start Gunicorn ────────────────────────────────────────────────────────────
CMD ["sh", "-c", "gunicorn wsgi:app --workers 2 --bind 0.0.0.0:$PORT --timeout 120"]
