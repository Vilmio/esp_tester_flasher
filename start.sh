#!/bin/bash

git checkout .
git pull

python3 webServerApp.py

exit $?
