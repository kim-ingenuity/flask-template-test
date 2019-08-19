#!/bin/bash

LGHTRED='\033[1;31m'
NC='\033[0m'

echo -e "Shutting down Flask API container with port $1"
NGINX_PORT=$1 docker-compose down && \
echo -e "${LGHTRED}Successful shutdown for the Flask API container on port $1"
