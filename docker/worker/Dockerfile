FROM ghcr.io/astral-sh/uv:python3.12-alpine
WORKDIR /api
COPY . .

RUN export PYTHONPATH="${PYTHONPATH}:/api/"
RUN uv sync --locked --no-group server
RUN python -m compileall -q ./src/

CMD ["uv", "run", "dramatiq", "src.entrypoints.worker", "--processes", "2", "--threads", "8"]
