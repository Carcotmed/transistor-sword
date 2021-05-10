import logging
from queue import Queue
from threading import Thread
import time
import board
import audiocore
import audiopwmio
import digitalio

class AudioThread(object):
    verbose = True
    thread = None
    queue = Queue()
    manualMode = False
    playNext = False

    def __init__(self, queueMaxSize = 50, emptyQueuewaitTime = 1):
        self.queue.maxsize = queueMaxSize
        self.thread = Thread(target=self.__work, args=(emptyQueuewaitTime,))
        self.thread.setDaemon(True)
        self.thread.start()

    def __work(self, sl):
        while(True):
            if not self.queue.empty():
                #Hay valores en la cola
                if (not self.manualMode or (self.manualMode and self.playNext)):
                    #O estamos en modo automático, o en manual con playNext activado
                    audioFile = self.queue.get()
                    logging.info("Audio Thread: Playing audio - "+str(audioFile))

                    #Required for CircuitPlayground Express
                    #speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
                    #speaker_enable.switch_to_output(value=True)

                    data = open("./audio_files/data_smoke_test_LDC93S1_pcms16le_1_16000.wav", "rb")
                    wav = audiocore.WaveFile(data)
                    a = audiopwmio.PWMAudioOut(board.SPEAKER)

                    a.play(wav)
                    while a.playing:
                        pass
                    
                    logging.info("Audio Thread: Finished audio - "+str(audioFile))
                    logging.info ("Audio Thread: Current queue size - "+str(self.queue.qsize()))
                    self.queue.task_done()
                    self.playNext = False
                else:
                    #Estamos en modo manual sin playNext activado
                    logging.info("Audio Thread: Awaiting manual trigger")
            else:
                logging.info("Audio Thread: Empty Queue")

        logging.info("Audio Thread: Sleeping for - "+str(sl)+"ms")
        time.sleep(sl)

    def setManualMode (self, val):
        self.manualMode = val

    def playNextAudio (self, val):
        self.playNext = True

    def put(self, audioFile, waitIfFull = True):
        self.queue.put(audioFile, waitIfFull)
        if self.verbose:
            logging.info ("Audio Thread: Added to queue - "+str(audioFile))
            logging.info ("Audio Thread: Current queue size - "+str(self.queue.qsize()))

if __name__ == '__main__':

    #audioThread = AudioThread()

    #audioThread.put("audio_files/data_smoke_test_LDC93S1_pcms16le_1_16000.wav")

    #samplerate, data = wavfile.read('./audio_files/data_smoke_test_LDC93S1_pcms16le_1_16000.wav')

    data = open("./audio_files/data_smoke_test_LDC93S1_pcms16le_1_16000.wav", "rb")
    print(data)