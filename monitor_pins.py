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

# Store lowest score in an array for each track
lowest_score = [10.0, 10.0]

# Debug to display sensor data or state on the screen when on. Set to False to disable
debugOn = False

# Load up WAV file
pygame.mixer.init()
play_sound = pygame.mixer.Sound("/home/hive/Scripts/CrowdCheer.wav")
play_sound.play()
start_sound = pygame.mixer.Sound("/home/hive/Scripts/racing-car-test.wav")


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
    # Function to display the time on the screen
    def Render(s, rgb, size):
        fnt = pygame.font.SysFont("Any", size * height // 1080)
        txt = fnt.render(s, True, rgb)
        return txt

    screen.fill((0, 0, 0))

    txtTim = Render(thisTime, (255, 255, 255), 728)
    # Center the text on the screen
    # This line of code calculates the vertical position of a text object on a surface. It subtracts the height of the text object
    # from the height of the surface, then divides the result by 2 to center the text vertically.
    # The result is stored in the variable h.
    h = (height - txtTim.get_height()) // 2
    # //: Divides the number on its left by the number on its right, rounds down the answer, and returns a whole number.
    w = (width - txtTim.get_width()) // 2
    # The code screen.blit(txtTim, (w, h)) is used to blit or display an image or a text on the screen at the specified coordinates (w, h).
    # In this specific case, txtTim is likely a text that needs to be displayed on the screen, and (w, h) represents the x and y position where the text will be placed.
    # By calling screen.blit(txtTim, (w, h)), the text stored in txtTim will be rendered onto the screen at the specified position.
    screen.blit(txtTim, (w, h))

    # Render the text for the lowest score
    txtLowest = Render(
        "Best "
        + "{:.3f}".format(lowest_score[0]).zfill(6)
        + "     Best "
        + "{:.3f}".format(lowest_score[1]).zfill(6),
        (255, 255, 255),
        400,
    )
    # Put the lowest score at the top of the screen
    screen.blit(txtLowest, (w, 0))

    # If debug is on, display the sensor data
    if debugOn:
        # Render the text for the sensor data
        txtDebug = Render(
            "PIN 11: " + str(GPIO.input(11)) + "   PIN 13: " + str(GPIO.input(13)),
            (255, 255, 255),
            400,
        )
        # Put the debug data at the bottom of the screen
        screen.blit(txtDebug, (w, height - txtDebug.get_height()))
        # And PIN 15 and 7
        txtDebug2 = Render(
            "PIN 15: " + str(GPIO.input(15)) + "   PIN 7: " + str(GPIO.input(7)),
            (255, 255, 255),
            400,
        )
        # Put the debug data at the bottom of the screen
        screen.blit(txtDebug2, (w, height - txtDebug.get_height() * 2))

    pygame.display.update()


# The main code to display the track timers on the screen
def Main():
    global lowest_score, track_timer_1, track_timer_2, debugOn, play_sound, start_sound, pi_pins

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
                and track_timer_2.get_time_elapsed_from_last_start() > 600
            ):
                pygame.display.set_mode((1, 1))
                display_active = False
                # Reset low scores back to 0.0
                lowest_score = [10.000, 10.000]
                # If the timer is still running after 600 seconds, stop it
                if track_timer_1.is_running():
                    track_timer_1.stop()
                if track_timer_2.is_running():
                    track_timer_2.stop()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    GPIO.cleanup()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    kz = 0
                    pygame.quit()
                    GPIO.cleanup()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        GPIO.cleanup()
                        sys.exit()
                    elif event.key == pygame.K_d:
                        # Toggle debug mode
                        if debugOn == True:
                            debugOn = False
                        else:
                            debugOn = True

            # Sleep a little while to give the CPU a break
            time.sleep(0.1)


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
        start_sound.play()
    # Check if the car was seen on PIN 15 Track 2
    elif channel == 15:
        # Reset the timer
        track_timer_2.reset()
        print("Track 2 Reset and starting")
        track_timer_2.start()
        start_sound.play()
    # Check if the car was seen on PIN 13 Track 1
    elif channel == 13:
        # Check if the car is already running
        if track_timer_1.start_time != 0:
            # Car is running, stop the timer
            track_timer_1.stop()
            start_sound.stop()
            print("Track 1 Time:", track_timer_1.time_elapsed_string)
            # Reset the timer - We don't want this as the screen will clear
            # track_timer_1.reset()
            # If the time is lower than the lowest score, play the music
            if track_timer_1.get_time_elapsed() < lowest_score[0]:
                print("New low score!")
                lowest_score[0] = track_timer_1.get_time_elapsed()
                # Play the music
                play_sound.play()
                # pygame.mixer.music.load(music[pi_pin_index])
                # pygame.mixer.music.play()
    # Check if the car was seen on PIN 7 Track 2
    elif channel == 7:
        # Check if the car is already running
        if track_timer_2.start_time != 0:
            # Car is running, stop the timer
            track_timer_2.stop()
            start_sound.stop()
            print("Track 2 Time:", track_timer_2.time_elapsed_string)
            # If the time is lower than the lowest score, play the music
            if track_timer_2.get_time_elapsed() < lowest_score[1]:
                print("New low score!")
                lowest_score[1] = track_timer_2.get_time_elapsed()
                play_sound.play()


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
