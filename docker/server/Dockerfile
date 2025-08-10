FROM ghcr.io/astral-sh/uv:python3.12-alpine
WORKDIR /api
COPY . .

RUN export PYTHONPATH="${PYTHONPATH}:/api/"
RUN uv sync --locked --all-groups
RUN python -m compileall -q ./src/
EXPOSE 8000

CMD ["uv", "run", "granian", "--interface", "asgi", "src.entrypoints.server:app",\
"--host", "0.0.0.0", "--workers", "1", "--runtime-threads", "1", "--no-reload"]
