#!/bin/bash
# Start ML API for development
if ! docker network ls --format '{{.Name}}' | grep -q '^app-shared-network-prod$'; then
    docker network create --driver bridge --attachable app-shared-network-prod
fi
docker compose -f docker-compose.prod.yaml --env-file .env.prod -p ml-api-prod up -d
