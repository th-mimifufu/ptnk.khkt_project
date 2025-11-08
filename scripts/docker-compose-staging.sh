#!/bin/bash
# Start ML API for staging
docker compose -f docker-compose.staging.yaml --env-file .env.staging -p ml-api-staging up -d