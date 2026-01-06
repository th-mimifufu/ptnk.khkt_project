#!/bin/bash
# Start ML API for staging

# Create network only if it doesn't exist
if ! docker network ls --format '{{.Name}}' | grep -q '^backend-swarm-network-staging$'; then
    docker network create --driver overlay --attachable backend-swarm-network-staging
fi

docker stack deploy -c docker-compose.swarm.staging.yaml ml-swarm-staging --detach=false