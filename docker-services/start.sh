#!/bin/bash

LGHTGREEN='\033[1;32m'
NC='\033[0m'

echo -e "Starting up Flask API container with port $1"
NGINX_PORT=$1 docker-compose up --build -d && \
echo -e "${LGHTGREEN}Flask API container is up and running on port $1"
