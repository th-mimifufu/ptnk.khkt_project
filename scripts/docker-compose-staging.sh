#!/bin/bash
# Start ML API for staging
if ! docker network ls --format '{{.Name}}' | grep -q '^backend-network-staging$'; then
    docker network create --driver bridge --attachable backend-network-staging
fi
docker compose -f docker-compose.staging.yaml --env-file .env.staging -p ml-api-staging up -d