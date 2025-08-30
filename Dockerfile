# ================================
# BUILDER STAGE
# ================================
FROM python:3.10-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# ================================
# RUNTIME STAGE
# ================================
FROM python:3.10-slim as runtime

# Build arguments for versioning
ARG APP_VERSION=latest
ARG BUILD_DATE
ARG VCS_REF

# Labels for image metadata
LABEL org.opencontainers.image.title="Sistema Produtos" \
      org.opencontainers.image.description="Sistema de Produtos Django Application" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="Meitans"

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_VERSION=${APP_VERSION}

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gettext \
        curl \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set work directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . /app/

# Copy entrypoint script
COPY --chown=appuser:appuser docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/healthz/ || exit 1

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--worker-class", "gthread", "--threads", "2", "--timeout", "120", "--keep-alive", "5", "--max-requests", "1000", "--max-requests-jitter", "100", "sistema_produtos.wsgi:application"]
