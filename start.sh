#!/bin/sh
# This script will start the pygame timer application. 
# On 2023-07-30 I found the pygame app crashed due to X display error.
# So now I've put it in a loop to restart the application when it fails.

while true
do
    ./monitor_pins.py
    # Sleep 5 seconds to give time for everything to shutdown and clean up
    sleep 5
done

# I'll still need to check the terminal displau to see if it's running or how many times it crashed.
# I don't want to log to a file for fear the FS will fill up and cause a different crash.