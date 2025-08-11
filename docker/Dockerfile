FROM ghcr.io/astral-sh/uv:python3.12-alpine
WORKDIR /api
COPY . .

RUN export PYTHONPATH="${PYTHONPATH}:/api/"
RUN uv sync --locked --all-groups
RUN python -m compileall -q ./src/
