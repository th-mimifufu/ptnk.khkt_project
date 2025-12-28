#!/bin/bash
# Start ML API for development
if ! docker network ls --format '{{.Name}}' | grep -q '^app-shared-network-dev$'; then
    docker network create --driver bridge --attachable app-shared-network-dev
fi
docker compose -f docker-compose.dev.yaml --env-file .env.dev -p ml-api-dev up -d
