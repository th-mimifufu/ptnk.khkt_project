#!/bin/bash
# Start ML API for development
docker compose -f docker-compose.prod.yaml --env-file .env.prod -p ml-api-prod up -d
