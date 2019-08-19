#!/bin/bash

echo "Starting server"
supervisord --configuration=docker-services/supervisor/supervisord.conf
