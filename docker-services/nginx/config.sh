#!/bin/bash

echo "Loading of default environment variables for nginx"
if [ "$NGINX_PROXY_READ_TIMEOUT" = "" ]
then
    echo "NGINX_PROXY_READ_TIMEOUT wasn't initally set. Defaulting NGINX_PROXY_READ_TIMEOUT to '600s'"
    export NGINX_PROXY_READ_TIMEOUT='600s'
else
    echo "NGINX_PROXY_READ_TIMEOUT was set to '"$NGINX_PROXY_READ_TIMEOUT"'"
fi

if [ "$NGINX_PROXY_CONNECT_TIMEOUT" = "" ]
then
    echo "NGINX_PROXY_CONNECT_TIMEOUT wasn't initally set. Defaulting NGINX_PROXY_CONNECT_TIMEOUT to '600s'"
    export NGINX_PROXY_CONNECT_TIMEOUT='600s'
else
    echo "NGINX_PROXY_CONNECT_TIMEOUT was set to '"$NGINX_PROXY_CONNECT_TIMEOUT"'"
fi

echo "Creating nginx configuration file"
sed -e "s/\${NGINX_PROXY_READ_TIMEOUT}/$NGINX_PROXY_READ_TIMEOUT/g" -e "s/\${NGINX_PROXY_CONNECT_TIMEOUT}/$NGINX_PROXY_CONNECT_TIMEOUT/g" docker-services/nginx/template.txt > docker-services/nginx/flask-api

echo "Configuring nginx"
cp docker-services/nginx/flask-api /etc/nginx/sites-available/
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/flask-api /etc/nginx/sites-enabled
