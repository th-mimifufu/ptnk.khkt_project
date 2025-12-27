#!/bin/bash
# Start ML API for testelopment
if ! docker network ls --format '{{.Name}}' | grep -q '^app-shared-network-test$'; then
    docker network create --driver bridge --attachable app-shared-network-test
fi
docker compose -f docker-compose.test.yaml --env-file .env.test -p ml-api-test up -d
