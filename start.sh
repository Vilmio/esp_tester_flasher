#!/bin/bash

sudo -E -u test git checkout .
sudo -E -u test git pull

python3 webServerApp.py

exit $?
