#!/usr/bin/env python3

import signal
import RPi.GPIO as GPIO
from ai import show_ai
from comic import show_comic
from status import show_status

pins = [5, 6, 16, 24]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def handle_event(pin):
    match pin:
        case 5:
            print('showing ai image')
            show_ai()
        case 6:
            print('showing comic')
            show_comic()
        case 24:
            print('showing status')
            show_status()

for pin in pins:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_event, bouncetime=250)

print('listing for inky button events')
signal.pause()
