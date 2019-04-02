#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /home/pi
sudo -u pi ./scan_for_tags.py > /home/pi/player.log 2>&1
