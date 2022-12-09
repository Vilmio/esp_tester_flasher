#!/bin/bash

sudo -u test git checkout .
sudo -u test git pull

sudo -u test python3 webServerApp.py

exit $?
