#!/bin/bash

apt-get update
apt-get install -y unzip curl telnet nano

unzip docker-services/oracle/instantclient-sqlplus-linux.x64-18.3.0.0.0dbru.zip -d /opt/oracle
sh -c "echo /opt/oracle/instantclient_18_3 > /etc/ld.so.conf.d/oracle-instantclient.conf" && ldconfig
echo 'export PATH=/opt/oracle/instantclient_18_3:$PATH' >> ~/.bashrc
source ~/.bashrc
