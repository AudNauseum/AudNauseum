from metronome import Metronome

'''Loop is the primary object that gets passed from state to state'''
class Loop:
    def __init__(self):
        self.trackList = []   #List of Tracks in the loop
        self.met = Metronome(100, 4)
        self.fx = FxSettings()
    
    def addTrack(self, track):
        self.trackList.append(track)

    def removeTrack(self, track):
        self.trackList.remove(track) 
    
'''Loops manage Tracks. A track is an audio stream and a set of 
    parameters that allow different tracks to sync together'''
class Track:
    def __init__(self):
        self._filename = None          #File Identifier 
        self._sampleRate = 44100
        self._bitDepth = 16
        self._bpm = None
        self._length_in_beats = None
        self._length_in_ms = None
        self._isStereo = False
    
    @property
    def filename(self):
        return self._filename

    @filename.setter 
    def filename(self, name):
        self._filename = name
    
    @property
    def bpm(self):
        return self._bpm
    
    @bpm.setter
    def bpm(self, bpm):
        self._bpm = bpm

    @property
    def length_in_beats(self):
        return self._length_in_beats

    @length_in_beats.setter
    def length_in_beats(self, beats):
        self._length_in_beats = beats
    

'''FxSettings are an attribute of both Tracks and Loops. 
    Only "_slip" doesn't make sense when applying effects to loops'''
class FxSettings:
    def __init__(self, vol=0.5, pan=0.5, isReversed=False, pitchAdjust=0, slip=0):
        self._volume = vol
        self._pan = pan
        self._isReversed = isReversed
        self._pitchAdjust = pitchAdjust
        self._slip = slip
    
    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, vol):
        self._volume = vol
    
    @property
    def pan(self):
        return self._pan

    @pan.setter    
    def pan(self, pan):
        self._pan = pan
    
    @property
    def isReversed(self):
        return self._isReversed

    def toggleIsReversed(self):
        self._isReversed = not(self._isReversed)
    
    @property
    def pitchAdjust(self):
        return self._pitchAdjust

    @pitchAdjust.setter
    def pitchAdjust(self, adj):
        self._pitchAdjust = adj

    @property
    def slip(self):
        return self._slip

    @slip.setter
    def slip(self, slip):
        self._slip = slip