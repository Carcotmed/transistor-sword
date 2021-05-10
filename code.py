import os
import busio
import board
import audiocore
import audiopwmio
import digitalio
#import adafruit_character_lcd.character_lcd as characterlcd
#THIS ONE
import adafruit_character_lcd.character_lcd_i2c as character_lcd

from random import randint
import time

lcd_columns = 16
lcd_rows = 4

i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2)

a = audiopwmio.PWMAudioOut(board.SPEAKER)

#lcd_rs = digitalio.DigitalInOut(board.D26)
#lcd_en = digitalio.DigitalInOut(board.D19)
#lcd_d7 = digitalio.DigitalInOut(board.D27)
#lcd_d6 = digitalio.DigitalInOut(board.D22)
#lcd_d5 = digitalio.DigitalInOut(board.D24)
#lcd_d4 = digitalio.DigitalInOut(board.D25)

#lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

normalAudioFiles = []
drunkAudioFiles = []
audioFiles = []

for file in os.listdir("./audio_files/normal"):
    normalAudioFiles.append((file, "./audio_files/normal"+file))

for file in os.listdir("./audio_files/drunk"):
    drunkAudioFiles.append((file, "./audio_files/drunk"+file))

chosenAudio = 0
normalColorRGB = (66, 245, 212)
drunkColorRGB = (209, 19, 19)
countDownToAutomaticVoiceline = 2000
chosenTextDisplacement = -1

#TODO GET VALUES FROM THE REAL BOARD
#SWITCHES
SWITCH_MODO_MANUAL = DigitalInOut(board.SWITCH)
SWITCH_MODO_MANUAL.direction = Direction.INPUT
SWITCH_MODO_MANUAL.pull = Pull.UP

SWITCH_DRUNK = DigitalInOut(board.SWITCH)
SWITCH_DRUNK.direction = Direction.INPUT
SWITCH_DRUNK.pull = Pull.UP

#BOTONES
BOTON_MANUAL_PULSADO = DigitalInOut(board.SWITCH)
BOTON_MANUAL_PULSADO.direction = Direction.INPUT
BOTON_MANUAL_PULSADO.pull = Pull.UP
prev_BOTON_MANUAL_PULSADO_state = BOTON_MANUAL_PULSADO.value

BOTON_ARRIBA_PULSADO = DigitalInOut(board.SWITCH)
BOTON_ARRIBA_PULSADO.direction = Direction.INPUT
BOTON_ARRIBA_PULSADO.pull = Pull.UP
prev_BOTON_ARRIBA_PULSADO_state = BOTON_ARRIBA_PULSADO.value

BOTON_ABAJO_PULSADO = DigitalInOut(board.SWITCH)
BOTON_ABAJO_PULSADO.direction = Direction.INPUT
BOTON_ABAJO_PULSADO.pull = Pull.UP
prev_BOTON_ABAJO_PULSADO_state = BOTON_ABAJO_PULSADO.value

def duty_cycle(percent):
    return int(percent / 100.0 * 65535.0)

def playAudio():
    currentlyChosenAudio = audioFiles[chosenAudio%len(audioFiles)]
    data = open("./audio_files/"+currentlyChosenAudio, "rb")

    wav = audiocore.WaveFile(data)

    #TODO VER SI LA MISMA SEÑAL PWM SE PUEDE USAR TANTO PARA AUDIO COMO PARA LEDS

    if a.playing(): a.stop()

    a.play(wav)
    
    chosenTextDisplacement = 0
    #while a.playing:
    #    time.sleep(5)
    #    lcd.move_left()
    #    #SI MUEVE TODA LA PANTALLA, LO HAGO MANUAL
    #pass

def showCurrentAudioScreen():
    previousCurrentlyChosenAudio = audioFiles[chosenAudio-1%len(audioFiles)]
    currentlyChosenAudio = audioFiles[chosenAudio%len(audioFiles)]
    nextCurrentlyChosenAudio = audioFiles[chosenAudio+1%len(audioFiles)]

    #PANTALLA DE 16 CARACTERES Y 4 LINEAS
    #16X4

    linea1 = "--Transist-OS---" if not SWITCH_DRUNK.value else "--7r4n5157-05---"
    linea2 = previousCurrentlyChosenAudio[0:16]
    linea4 = nextCurrentlyChosenAudio[0:16]
    if a.playing() and chosenTextDisplacement<0:
        chosenTextDisplacement +=1
        linea3 = (currentlyChosenAudio+" ")[chosenTextDisplacement%len(currentlyChosenAudio):14+chosenTextDisplacement%len(currentlyChosenAudio)]
    else:
        linea3 = currentlyChosenAudio[0:14]+"<-"

    lcd.message = linea1+"\n"+linea2+"\n"+linea3+"\n"+linea4



while True:

    if SWITCH_DRUNK.value:
        audioFiles = drunkAudioFiles
    else:
        audioFiles = normalAudioFiles

    if SWITCH_MODO_MANUAL.value:
        countDownToAutomaticVoiceline = 2000
        #MODO MANUAL
        if (BOTON_MANUAL_PULSADO and not prev_BOTON_MANUAL_PULSADO_state):
            #playAudio(currentlyChosenAudio)
            prev_BOTON_MANUAL_PULSADO_state = BOTON_MANUAL_PULSADO.value
            pass
        else:
            if (BOTON_ARRIBA_PULSADO and not prev_BOTON_ARRIBA_PULSADO_state):
                chosenAudio+=1
                chosenTextDisplacement = -1
                prev_BOTON_ARRIBA_PULSADO_state = BOTON_ARRIBA_PULSADO.value
            elif (BOTON_ABAJO_PULSADO and not prev_BOTON_ABAJO_PULSADO_state):
                chosenAudio-=1
                chosenTextDisplacement = -1
                prev_BOTON_ABAJO_PULSADO_state = BOTON_ABAJO_PULSADO.state
    else:
        #MODO AUTOMÁTICO
        if countDownToAutomaticVoiceline <= 0:
            countDownToAutomaticVoiceline = 2000
            chosenAudio = randint(0,len(audioFiles)-1)
            #playAudio()
        else:
            countDownToAutomaticVoiceline-=1

    showCurrentAudioScreen()

    


    
