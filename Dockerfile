# Install python and uv
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY src/ ./src/
COPY data/ ./data/models/

EXPOSE 8080

ENTRYPOINT ["uv", "run", "uvicorn", "ml_engineer_exam.api.app:app", "--host", "0.0.0.0", "--port", "8080"]
