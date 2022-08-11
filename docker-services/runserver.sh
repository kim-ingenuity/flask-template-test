#!/bin/bash

. ./docker-services/nginx/config.sh

if [ "$UPDATE_DATABASE_TABLES_DURING_CONTAINER_RUN" = "True" ]
then
    echo "UPDATE_DATABASE_DURING_CONTAINER_RUN was set to True. Updating database table structures"
    python manage.py db upgrade
else
    echo "Database updating is disabled. To enable, set the environment variable UPDATE_DATABASE_TABLES_DURING_CONTAINER_RUN to True"
fi

if [ "$LOAD_FIXTURES_DURING_CONTAINER_RUN" = "True" ]
then
    echo "LOAD_FIXTURES_DURING_CONTAINER_RUN was set to True. Loading fixtures to database"
    python manage.py load_data
else
    echo "Fixture loading is disabled. To enable, set the environment variable LOAD_FIXTURES_DURING_CONTAINER_RUN to True"
fi

if [ "$GUNICORN_WORKERS" = "" ]
then
    echo "GUNICORN_WORKERS wasn't initally set. Defaulting GUNICORN_WORKERS to '4'"
    export GUNICORN_WORKERS=4
else
    echo "GUNICORN_WORKERS was set to '"$GUNICORN_WORKERS"'"
fi

if [ "$GUNICORN_TIMEOUT" = "" ]
then
    echo "GUNICORN_TIMEOUT wasn't initally set. Defaulting GUNICORN_TIMEOUT to '600'"
    export GUNICORN_TIMEOUT=600
else
    echo "GUNICORN_TIMEOUT was set to '"$GUNICORN_TIMEOUT"'"
fi

if [ "$LOGGING_LEVEL" = "" ]
then
    echo "LOGGING_LEVEL wasn't initally set. Defaulting LOGGING_LEVEL to 'info'"
    export LOGGING_LEVEL='info'
else
    echo "LOGGING_LEVEL was set to '"$LOGGING_LEVEL"'"
fi

echo "Starting server"
supervisord --configuration=docker-services/supervisor/supervisord.conf
