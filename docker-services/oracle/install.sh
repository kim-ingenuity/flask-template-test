#!/bin/bash

echo "Install cx-Oracle python library"
pip install 'cx-Oracle==7.1.2'

echo "Installing Oracle instantclient-basic installation dependencies"
apt-get update
apt-get install -y libaio1 unzip

echo "Installing Oracle instantclient-basic"
unzip docker-services/oracle/instantclient-basic-linux.x64-18.3.0.0.0dbru.zip -d /opt/oracle
apt-get remove -y unzip
sh -c "echo /opt/oracle/instantclient_18_3 > /etc/ld.so.conf.d/oracle-instantclient.conf" && ldconfig
