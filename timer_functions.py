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

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        self.time_elapsed = self.end_time - self.start_time
        self.time_elapsed_string = "{:.3f}".format(self.time_elapsed)
        return self.time_elapsed_string

    def get_time(self):
        self.time_elapsed = time.time() - self.start_time
        self.time_elapsed_string = "{:.3f}".format(self.time_elapsed)
        return self.time_elapsed_string

    def reset(self):
        self.start_time = time.time()
        self.end_time = time.time()
        self.time_elapsed = 0.0
        self.time_elapsed_string = "0.000"


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
    print("Waitingfor 5 seconds")
    time.sleep(5)
    print("Stopping timer")
    print(timer.stop())
    print("Resetting timer")
    timer.reset()
    print("Getting time")
    print(timer.get_time())
    print("Done testing timer_functions.py")
