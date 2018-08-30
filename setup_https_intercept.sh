#!/bin/sh
mkdir -p "$HOME/.purp"
openssl genrsa -out "$HOME/.purp/ca.key" 2048
openssl req -new -x509 -days 3650 -key "$HOME/.purp/ca.key" -out "$HOME/.purp/ca.crt" -subj "/CN=proxy CA"
openssl genrsa -out "$HOME/.purp/cert.key" 2048
mkdir -p "$HOME/.purp/certs"
