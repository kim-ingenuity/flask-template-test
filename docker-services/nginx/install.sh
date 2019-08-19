#!/bin/bash

echo "Installing nginx"
apt-get update
apt-get install -y nginx

echo "Configuring nginx"
cp docker-services/nginx/flask-api /etc/nginx/sites-available/
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/flask-api /etc/nginx/sites-enabled

## Uncomment to write the nginx logs to the Docker container
# echo "Linking nginx logs"
# ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log
