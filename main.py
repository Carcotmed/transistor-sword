import threading
from gpiozero import Button
from audio_thread import AudioThread
import simpleaudio
#GPIO MANAGEMENT FOR HILT BUTTONS

#LCD SCREEN FOR SETUP/AUDIO SELECTION

#RASPBERRY PI

#SPEAKERS

#BATTERY


if __name__ == '__main__':
    print("patata")

    audioThread = new AudioThread()

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

        while True:

            if switch_random.is_active():
                #MODO RANDOM

            else:




    except:
        logging.warn('GPIO Transl.: No GPIO found')