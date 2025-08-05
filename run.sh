sudo docker compose -f ./payment-processor/docker-compose.yml up -d
uv run dramatiq src.worker &
uv run fastapi dev ./src/server.py --port 9999
