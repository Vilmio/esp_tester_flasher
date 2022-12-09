#!/bin/bash

sudo -E -u test git checkout .
sudo -E -u test git pull

sudo -E -u python3 webServerApp.py

exit $?
