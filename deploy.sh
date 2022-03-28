#!/bin/bash

echo ">>>>>>Starting deploy<<<<<<"

echo ">>>>>>Stopping port running server before..."
kill -9 `sudo lsof -t -i:8002`
echo ">>>>>>Create virtual env..."
python3 -m venv env

# source python env
echo ">>>>>>Sourcing python env..."
. env/bin/activate

# install requirements
pip install -r requirements.txt

# migrate model
echo "Migrate model..."
python manage.py migrate

# run server
echo "Run server..."
export BUILD_ID=dontKillMe
nohup python manage.py runserver 0:8002 > my.log 2>&1 &
