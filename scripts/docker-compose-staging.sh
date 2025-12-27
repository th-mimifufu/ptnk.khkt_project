#!/bin/bash
# Start ML API for staging
if ! docker network ls --format '{{.Name}}' | grep -q '^app-shared-network-staging$'; then
    docker network create --driver bridge --attachable app-shared-network-staging
fi
docker compose -f docker-compose.staging.yaml --env-file .env.staging -p ml-api-staging up -d