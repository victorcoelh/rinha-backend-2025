FROM ghcr.io/astral-sh/uv:python3.12-alpine
WORKDIR /api
COPY . .

RUN apk add --no-cache libffi-dev openssl-dev gcc musl-dev
RUN export PYTHONPATH="${PYTHONPATH}:/api/"
RUN uv sync --locked --no-group server

CMD ["uv", "run", "dramatiq", "src.entrypoints.worker", "--processes", "2", "--threads", "8"]
