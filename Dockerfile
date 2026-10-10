
# ---------- Build stage: install dependencies into a virtualenv ----------
FROM python:3.11-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install into /opt/venv (NOT /root/.local), so the files are readable by any user.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt


# ---------- Runtime stage: small image, non-root user ----------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Numeric UID/GID so Kubernetes can verify runAsNonRoot.
RUN groupadd --system --gid 10001 app \
 && useradd  --system --uid 10001 --gid app \
             --home-dir /app --no-create-home \
             --shell /usr/sbin/nologin app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=10001:10001 app ./app

USER 10001:10001

EXPOSE 8000

# `python -m uvicorn` avoids depending on a script path.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]