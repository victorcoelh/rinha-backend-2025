FROM ghcr.io/astral-sh/uv:python3.12-alpine
WORKDIR /api
COPY . .

#RUN chmod +x /api/run.sh
RUN apk add --no-cache libffi-dev openssl-dev gcc musl-dev
RUN export PYTHONPATH="${PYTHONPATH}:/api/"
RUN uv sync --locked --all-groups
EXPOSE 8000

CMD ["uv", "run", "granian", "--interface", "asgi", "src.entrypoints.server:app", "--host", "0.0.0.0"]
