
# Purp

## PURPOSE
Creation of an Intercepting Proxy Script in Python 3 with an interpreter with
basic command.

## REQUIREMENTS

* Python3
* OpenSSL

Additional requirements:
* Nmap
* Nikto

## INSTALLATION

1. Install the local certificate:
`./setup_https_intercept`

This script will create the necessary certificate but you need to install the
certificate on the browser for launch purp.

2. With the proxy activate on the browser on the port 8080 go on the page
`http://purp.ca`

It must be http and not https otherwise it will not intall the certificate on
the browser.

3. install the module in the requirements.txt
`pip -r install requirements.txt`

## USAGE

    

## NOTES


