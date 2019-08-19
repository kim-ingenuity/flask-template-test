#!/bin/bash

check_not_null()
{
    if [ "$1" != "''" ]
    then
        printf "true\n"
    else
        printf "false\n"
    fi
}

echo "Checking if Docker is already running..."
docker version

printf "\nChecking if container is running...\n"
printf "Flask API $1: "
check_not_null "'$(docker container ls  -q -f name=flask_apis_$1)'"
