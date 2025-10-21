#!/bin/bash
# Start ML API for development
docker compose -f docker-compose.dev.yaml --env-file .env.dev -p ml-api-dev up -d
