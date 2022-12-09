#!/bin/bash

sudo git checkout .
sudo git pull

sudo -u test python3 webServerApp.py

exit $?
