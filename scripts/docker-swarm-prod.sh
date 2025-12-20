#!/bin/bash
# Start ML API for prod

# Create network only if it doesn't exist
if ! docker network ls --format '{{.Name}}' | grep -q '^app-shared-network-prod$'; then
    docker network create --driver overlay --attachable app-shared-network-prod
fi

docker stack deploy -c docker-compose.swarm.prod.yaml ml-swarm-prod --detach=false