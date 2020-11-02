from threading import Thread
from time import sleep
import sounddevice as sd
import soundfile as sf

sd.default.samplerate = 44100


class Metronome:
    def __init__(self, bpm, beats, volume=0.5, countIn=False, isOn=False):
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

    def _aTimer(self, timeAtCursorMs, slip):
        # to get the timer to pick up wherever you are in the audio playback,
        # the cursor needs to get converted from a Numpy array index to an
        # elapsed time since the beginning of the loop. We can use the
        # beginning of the audio file as long as we adjust it by the "slip"
        # value in the track and can reasonably assume that all recordings
        # start at the beginning of a loop or any departure is reliably
        # captured by the "slip".
        filename1 = './resources/metronome/downBeat.wav'
        filename2 = './resources/metronome/beat.wav'
        # Extract data and sampling rate from file
        downBeat, fs = sf.read(filename1, dtype='float32')
        beat, fs = sf.read(filename2, dtype='float32')

        firstIter = True
        timeOffset = ((timeAtCursorMs / 1000) + slip)
        # print(f"timeOffset: {timeOffset}")
        if timeOffset == 0:
            nextBeat = 0
        else:
            # print(f"seconds per beat {60/self.bpm}")
            nextBeat = (int(timeOffset / (60/self.bpm)) + 1) % self.beats
            # print(f"nextBeat: {nextBeat}")
            # time_to_next_beat = (60/self.bpm) - timeOffset % (60/self.bpm)
            # print(f"Time to next beat: {time_to_next_beat}")
        while self.isOn:
            if firstIter:
                sleep(60/self.bpm - timeOffset % (60/self.bpm))
                firstIter = False
            else:
                sleep((60/self.bpm))
            if(nextBeat == 0):
                sd.play(downBeat, fs)
            else:
                sd.play(beat, fs)
            nextBeat = (nextBeat + 1) % self.beats

    def start(self, timeAtCursorMs=0, slip=0):
        Thread(target=self._aTimer, args=(timeAtCursorMs, slip)).start()


if __name__ == "__main__":
    myMetronome = Metronome(120, 4, isOn=True)
    myMetronome.start()
    sleep(30)
    myMetronome.isOn = False
