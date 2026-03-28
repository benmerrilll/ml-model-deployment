# Install python and uv
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev && uv pip install awslambdaric

COPY src/ ./src/
COPY data/models/ ./data/models/

ENV PYTHONPATH=/app/src

ENTRYPOINT ["/app/.venv/bin/python", "-m", "awslambdaric"]
CMD ["ml_engineer_exam.api.app.handler"]
