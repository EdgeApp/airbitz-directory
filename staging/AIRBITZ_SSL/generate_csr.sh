#!/bin/bash

openssl req -new -key apache.key -out airbitz.co.csr -config openssl.cnf -subj "/C=US/ST=California/L=San Diego/CN=airbitz.co/O=Airbitz. Inc"

openssl req -in airbitz.co.csr -text -noout