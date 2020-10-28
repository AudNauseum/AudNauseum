from threading import Thread
from time import sleep

class Metronome:
    def __init__(self, bpm, beats, volume = 0.5, countIn = False, isOn = False):
        self._bpm = bpm
        self._beats = beats
        self._volume = volume
        self._countIn = countIn
        self._isOn = isOn

    @property
    def bpm(self):
        return self._bpm
    
    @bpm.setter
    def bpm(self, bpm):
        self._bpm = bpm
    
    @property
    def beats(self):
        return self._beats
    
    @beats.setter
    def beats(self, beats):
        self._beats = beats
    
    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, vol):
        self._volume = vol

    @property
    def countIn(self):
        return self._countIn

    @countIn.setter
    def countIn(self, countIn):
        self._countIn = countIn

    @property
    def isOn(self):
        return self._isOn
    
    @isOn.setter
    def isOn(self, isOn):
        self._isOn = isOn

    def _aTimer(self, cursor):
        ##to get the timer to pick up wherever you are in the audio playing, 
        # the cursor needs to get converted from a Numpy array index to an 
        # elapsed time since the beginning of the loop. Since we will have 
        # the option to slip an audio file left and right, we cannot rely 
        # on the timing from the track. I haven't yet figured out how to do this. 
        currentBeat = 0
        while self.isOn:
            sleep(60/self.bpm)
            if(currentBeat == 0):
                print("\nDING ", end="")
            else:
                print("ding ", end="")
            currentBeat = (currentBeat + 1) % self.beats

    def start(self):
        Thread(target=self._aTimer).start()

if __name__ == "__main__":
    myMetronome = Metronome(110, 3, isOn=True)
    myMetronome.start()
    sleep(30)
    myMetronome.isOn = False