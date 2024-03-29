import json
from threading import Thread
from time import sleep
import sounddevice as sd
import soundfile as sf

sd.default.samplerate = 44100


class Metronome(object):
    def __init__(self, bpm=None, beats=None, volume=0.5, count_in=False,
                 is_on=False):
        self._bpm = bpm
        self._beats = beats
        self._volume = volume
        self._count_in = count_in
        self._is_on = is_on

    def to_dict(self):
        data = {}
        data['__type__'] = 'Metronome'
        data['bpm'] = self.bpm
        data['beats'] = self.beats
        data['volume'] = self.volume
        data['count_in'] = self.count_in
        data['is_on'] = self.is_on
        return data

    def from_dict(self, data):
        self.bpm = data['bpm']
        self.beats = data['beats']
        self.volume = data['volume']
        self.count_in = data['count_in']
        self.is_on = data['is_on']

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

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
    def count_in(self):
        return self._count_in

    @count_in.setter
    def count_in(self, count_in):
        self._count_in = count_in

    @property
    def is_on(self):
        return self._is_on

    @is_on.setter
    def is_on(self, is_on):
        self._is_on = is_on

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
        while self.is_on:
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
    myMetronome = Metronome(120, 4, is_on=True)
    print(myMetronome.reprJSON())
    myMetronome.start()
    sleep(30)
    myMetronome.is_on = False
