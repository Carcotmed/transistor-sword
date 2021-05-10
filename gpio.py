import logging
from gpiozero import Button

import sys

#https://gpiozero.readthedocs.io/en/stable/api_input.html

def gpio_translate ():

    try:

        #BUTTONS:
            #UP/DOWN: SELECT AUDIO
            #SWITCH: NORMAL/RED MODE
            #BUTTON: PLAY
            #SWITCH: RANDOM PLAY

        #GPIO Pins: 5, 6, 13, 19, 26
        button_up = Button(5)
        button_down = Button(6)
        switch_mode = Button(13)
        button_play = Button(19)
        switch_random = Button(26)

        buttons = []
        buttons.append(button_up)
        buttons.append(button_down)
        buttons.append(switch_mode)
        buttons.append(button_play)
        buttons.append(switch_random)

        #Button config
        for button in buttons:
            button.hold_repeat=False
            button.hold_time=0

        while True:
            if button_up.:
                logging.info('GPIO Transl.: Left')
            
            if button_down.is_held:
                logging.info('GPIO Transl.: Right')
            
            if switch_mode.is_held:
                logging.info('GPIO Transl.: Up')

            if button_play.is_held:
                logging.info('GPIO Transl.: Down')

            if switch_random.is_held:
                logging.info('GPIO Transl.: Enter')


    except:
        logging.warn('GPIO Transl.: No GPIO found')
        sys.exit()

