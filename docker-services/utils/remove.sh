#!/bin/bash

apt-get remove -y unzip curl telnet nano

rm /opt/oracle/instantclient_18_3/glogin.sql /opt/oracle/instantclient_18_3/libsqlplus.so
rm /opt/oracle/instantclient_18_3/libsqlplusic.so /opt/oracle/instantclient_18_3/sqlplus
rm /opt/oracle/instantclient_18_3/SQLPLUS_README
grep -v 'export PATH=/opt/oracle/instantclient_18_3:$PATH' ~/.bashrc > ~/.bashrc.tmp; mv ~/.bashrc.tmp ~/.bashrc
