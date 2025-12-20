#!/bin/bash
# Start ML API for staging

# Create network only if it doesn't exist
if ! docker network ls --format '{{.Name}}' | grep -q '^app-shared-network-staging$'; then
    docker network create --driver overlay --attachable app-shared-network-staging
fi

docker stack deploy -c docker-compose.swarm.staging.yaml ml-swarm-staging --detach=false