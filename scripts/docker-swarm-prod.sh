#!/bin/bash
# Start ML API for prod

# Create network only if it doesn't exist
if ! docker network ls --format '{{.Name}}' | grep -q '^backend-swarm-network-prod$'; then
    docker network create --driver overlay --attachable backend-swarm-network-prod
fi

docker stack deploy -c docker-compose.swarm.prod.yaml ml-swarm-prod --detach=false