
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
    
This script will create the necessary certificate but you need to install the certificate on the browser for launch purp.

2. Activate the on the browser configuration on the port 8080 and go to the page

`http://purp.ca`

It must be **http** and not https otherwise it will not intall the certificate on the browser.

3. Install the module in the requirements.txt

`pip -r install requirements.txt`

## USAGE

There are two different mode:
1. Intercepting
2. Sniffing

Launch purp with 

`python purp.py`
 
it will start the proxy in sniffing mode so you can see all the request and response.
Use the command help for the list of command availaible in the interpreter.

If you want to launch purp in intercepting mode add the i flag

`python purp.py -i`

The proxy will catch the request and you can decide to go on or modify the request and see the response in the console and on the browser.

