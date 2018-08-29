#!/bin/sh
username=$(whoami)
mkdir -p /home/$username/.purp
openssl genrsa -out /home/$username/.purp/ca.key 2048
openssl req -new -x509 -days 3650 -key /home/$username/.purp/ca.key -out /home/$username/.purp/ca.crt -subj "/CN=proxy CA"
openssl genrsa -out /home/$username/.purp/cert.key 2048
mkdir -p /home/$username/.purp/certs
