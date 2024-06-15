#!/bin/sh
# This script will start the pygame timer application. 
# On 2023-07-30 I found the pygame app crashed due to X display error.
# So now I've put it in a loop to restart the application when it fails.
cd /home/hive/Scripts

while true
do
    ./monitor_pins.py
    echo "Script stopped! waiting 30 seconds then trying again"
    # Sleep 30 seconds to give time for everything to shutdown and clean up
    # AND to give time for a normal exit by operator to take control before restart.
    sleep 30
done

# I'll still need to check the terminal displau to see if it's running or how many times it crashed.
# I don't want to log to a file for fear the FS will fill up and cause a different crash.
