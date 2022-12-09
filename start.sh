#!/bin/bash

sudo -u test git checkout .
sudo -u test git pull

python3 webServerApp.py

exit $?
