#!/usr/bin/python3
# This file is imported by the main program and contains the object:
#   - track_timer - This will be used to track the time of the racecar timer
#

import time


# Create object to track the time of the racecar timer
class track_timer:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = time.time()
        self.time_elapsed = 0.0
        self.time_elapsed_string = "0.000"
        # Boolean to track if the timer is running
        self.running = False

    def start(self):
        self.start_time = time.time()
        self.running = True

    def is_running(self):
        return self.running

    # This function will return the time elapsed as number of seconds. Only used after timer has stopped.
    def get_time_elapsed(self):
        return round(self.time_elapsed, 3)

    def stop(self):
        self.end_time = time.time()
        self.time_elapsed = self.end_time - self.start_time
        self.time_elapsed_string = "{:.3f}".format(self.time_elapsed).zfill(6)
        self.running = False
        return self.time_elapsed_string

    def get_time(self):
        # Only return the time if the timer is running
        if self.running == True:
            self.time_elapsed = time.time() - self.start_time
            # If time_elapsed is greater then 99.999, set it to 99.999
            if self.time_elapsed > 99.999:
                self.time_elapsed = 99.999
            # format the string to 00.000
            self.time_elapsed_string = "{:.3f}".format(self.time_elapsed).zfill(6)
            return self.time_elapsed_string
        else:
            return self.time_elapsed_string

    def get_time_elapsed_from_last_start(self):  # get_time_elapsed_from_last_start
        return time.time() - self.start_time

    def reset(self):
        self.start_time = time.time()
        self.end_time = time.time()
        self.time_elapsed = 0.0
        self.time_elapsed_string = "0.000"
        self.running = False


if __name__ == "__main__":
    # This is a test function to test the timer
    # It will only be executed if this file is run directly.
    # It will not be executed if this file is imported.
    print("Testing timer_functions.py")
    print("Creating timer object")
    timer = track_timer()
    print("Starting timer")
    timer.start()
    print("Getting time")
    print(timer.get_time())
    print("Waiting for 5 seconds")
    time.sleep(5)
    print("Stopping timer")
    print(timer.stop())
    print("Resetting timer")
    timer.reset()
    print("Getting time")
    print(timer.get_time())
    print("Done testing timer_functions.py")
