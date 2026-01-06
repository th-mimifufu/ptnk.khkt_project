#!/bin/bash
# Start ML API for development
if ! docker network ls --format '{{.Name}}' | grep -q '^backend-network-prod$'; then
    docker network create --driver bridge --attachable backend-network-prod
fi
docker compose -f docker-compose.prod.yaml --env-file .env.prod -p ml-api-prod up -d
