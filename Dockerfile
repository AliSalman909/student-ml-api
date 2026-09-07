# Pinned to an explicit minor version for reproducible builds.
# "python:latest" is deliberately avoided: it moves without warning.
FROM python:3.12-slim

# Build metadata, supplied by the release workflow (see Part 23 OCI labels).
ARG APP_VERSION=dev
ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.title="student-ml-api" \
      org.opencontainers.image.description="Simple prediction API for the MLOps workflow exercise" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.source="https://github.com/AliSalman909/student-ml-api"

# Do not write .pyc files, and stream logs straight to stdout so that
# "docker logs" shows output immediately instead of buffering it.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencies are copied and installed before the application code so that
# this expensive layer stays cached when only app.py changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application files, ordered least-frequently-changed first.
COPY VERSION .
COPY app.py .

# Run as an unprivileged user rather than root.
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Bind to 0.0.0.0 so the service is reachable from outside the container.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
