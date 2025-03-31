FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Copy only dependency files first
COPY pyproject.toml poetry.lock ./

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libcairo2 \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry install --no-interaction --no-ansi \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY facturaization/ ./facturaization/
COPY alembic.ini ./

EXPOSE 8000