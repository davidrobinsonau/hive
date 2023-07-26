#!/usr/bin/python3
import RPi.GPIO as GPIO # Import the Raspberry Pi GPIO Library

# Setup GPIO Board settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pi_pins = [7,11,13,15] # This is the 4 pins we are monitoring

def button_callback(channel):
    # Print out the Pi PIN that detected the 3.3V
    # print(channel)
    # Print out the location in the list. Used for music
    pi_pin_index = pi_pins.index(channel)
    print("Car was seen on PIN:" , channel, pi_pin_index, ". ")


# Set pins to be INPUT and down
for pi_pin in pi_pins:
    GPIO.setup(pi_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Setup pin event monitoring
    GPIO.add_event_detect(pi_pin,GPIO.BOTH,button_callback, bouncetime=100)

# Pause Script for Input. As everything is a callback function, we only need to wait. 
message = input("Press Enter to stop Audio Button App and cleanup Application. This will load Login prompt:")

GPIO.cleanup()


