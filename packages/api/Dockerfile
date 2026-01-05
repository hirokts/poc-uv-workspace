FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY packages ./packages

WORKDIR /app/packages/api
RUN uv sync --locked --no-dev

EXPOSE 8000
CMD ["uv", "run", "api"]