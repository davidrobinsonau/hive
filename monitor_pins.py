#!/usr/bin/python3
import RPi.GPIO as GPIO  # Import the Raspberry Pi GPIO Library
import timer_functions as timer  # Import the timer_functions.py file
import text_display as textdisplay  # Import the text_display.py file
import os
import pygame, sys
from pygame.locals import *
import time

# Setup GPIO Board settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pi_pins = [7, 11, 13, 15]  # This is the 4 pins we are monitoring

# Track 1
# PIN 11 - Start
# PIN 13 - Stop

# Track 2
# PIN 15 - Start
# PIN 7 - Stop


# Create objects to track the time of each track
track_timer_1 = timer.track_timer()  # Track 1
track_timer_2 = timer.track_timer()  # Track 2


def FindDisplayDriver():
    for driver in ["fbcon", "directfb", "svgalib"]:
        if not os.getenv("SDL_VIDEODRIVER"):
            os.putenv("SDL_VIDEODRIVER", driver)
        try:
            pygame.display.init()
            return True
        except pygame.error:
            pass
    return False


def ShowClock(screen, width, height, thisTime):
    def Render(s, rgb, size):
        fnt = pygame.font.SysFont("Any", size * height // 1080)
        txt = fnt.render(s, True, rgb)
        return txt

    screen.fill((0, 0, 0))

    txtTim = Render(thisTime, (255, 255, 255), 728)
    h = (height - txtTim.get_height()) // 2
    w = (width - txtTim.get_width()) // 2
    screen.blit(txtTim, (w, h))

    pygame.display.update()


# The main code to display the track timers on the screen
def Main():
    if not FindDisplayDriver():
        print("Failed to initialise display driver")
    else:
        width = pygame.display.Info().current_w
        height = pygame.display.Info().current_h
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        display_active = True
        ShowClock(screen, width, height, "On your Marks")

        while True:
            # Check if the timer is running
            if track_timer_1.is_running() or track_timer_2.is_running():
                # Check if display is active
                if display_active == False:
                    pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    display_active = True
                # Get the string from both timers
                track_1_time = track_timer_1.get_time()
                track_2_time = track_timer_2.get_time()
                screen_message = track_1_time + "   " + track_2_time
                ShowClock(screen, width, height, screen_message)

            # If the track timers have not run for 10 minutes, hide pygame window
            if display_active == True and (
                track_timer_1.get_time_elapsed_from_last_start() > 600
                or track_timer_2.get_time_elapsed_from_last_start() > 600
            ):
                pygame.display.set_mode((1, 1))
                display_active = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    GPIO.cleanup()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                    kz = 0
                    pygame.quit()
                    GPIO.cleanup()
                    sys.exit()
            # Sleep a little while to give the CPU a break
            time.sleep(0.2)


def button_callback(channel):
    # Print out the Pi PIN that detected the 3.3V
    # print(channel)
    # Print out the location in the list. Used for music
    pi_pin_index = pi_pins.index(channel)
    print("Car was seen on PIN:", channel, pi_pin_index, ". ")

    # Check if the car was seen on PIN 11 Track 1
    if channel == 11:
        # Reset the timer
        track_timer_1.reset()
        print("Track 1 Reset and starting")
        track_timer_1.start()
    # Check if the car was seen on PIN 15 Track 2
    elif channel == 15:
        # Reset the timer
        track_timer_2.reset()
        print("Track 2 Reset and starting")
        track_timer_2.start()
    # Check if the car was seen on PIN 13 Track 1
    elif channel == 13:
        # Check if the car is already running
        if track_timer_1.start_time != 0:
            # Car is running, stop the timer
            track_timer_1.stop()
            print("Track 1 Time:", track_timer_1.time_elapsed_string)
            # Reset the timer - We don't want this as the screen will clear
            # track_timer_1.reset()
    # Check if the car was seen on PIN 7 Track 2
    elif channel == 7:
        # Check if the car is already running
        if track_timer_2.start_time != 0:
            # Car is running, stop the timer
            track_timer_2.stop()
            print("Track 2 Time:", track_timer_2.time_elapsed_string)


# Set pins to be INPUT and down
for pi_pin in pi_pins:
    GPIO.setup(pi_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Setup pin event monitoring
    GPIO.add_event_detect(pi_pin, GPIO.BOTH, button_callback, bouncetime=100)


if __name__ == "__main__":
    pygame.init()
    Main()
    pygame.quit()
    GPIO.cleanup()
