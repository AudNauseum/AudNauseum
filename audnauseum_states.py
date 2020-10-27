from enum import Enum, auto

'''Loop is the primary object that gets passed from state to state'''
class Loop:
    def __init__(self):
        self.trackList = []   #List of Tracks in the loop
        self.met = Metronome()
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
    
    def calcBpm(self):
        ## length of clip in milliseconds / beats * 60 * 1000
        ## Might be useful so you don't have to input track info that can be calculated.  
        pass

    def calcBeats(self):
        ##length of clip in milliseconds / 1000 / bpm / 60
        ##If inheriting the bpm from a loop, reduces user work
        pass  

'''Metronome is an attribute of a Loop that indicates when 
    Metronome Clicks should play'''
class Metronome:
    def __init__(self):
        self._bpm = 0                #Beats per Minute
        self._timeSigTop = 4         #Beats per Measure
        self._metVolume = 0.5
        self._countIn = False        #Count in one measure before recording starts
        self._isOn = False
    
    @property
    def bpm(self):
        return self._bpm

    @bpm.setter
    def bpm(self, bpm):
        self._bpm = bpm
    
    @property
    def timeSigTop(self):
        return self._timeSigTop
    
    @timeSigTop.setter
    def timeSigTop(self, top):
        self._timeSigTop = top
    
    @property
    def metVolume(self):
        return self._metVolume

    @metVolume.setter
    def metVolume(self, vol):
        self._metVolume = vol
    
    @property
    def countIn(self):
        return self._countIn
    
    def toggleCountIn(self):
        self._countIn = not(self._countIn)
    
    @property
    def isOn(self):
        return self._isOn

    def toggleIsOn(self):
        self._isOn = not(self._isOn)

'''FxSettings are an attribute of both Tracks and Loops. 
    Only "_slip" doesn't make sense when applying effects to loops'''
class FxSettings:
    def __init__(self):
        self._volume = 0.5
        self._pan = 0.5
        self._isReversed = False
        self._pitchAdjust = 0
        self._slip = 0
    
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

'''An Enumerated List of available states of the Audio Looper'''
class State(Enum):
    IDLE = auto()
    LOADED = auto()
    PAUSED = auto()
    PLAYING = auto()
    RECORDING = auto()
    PLAYING_AND_RECORDING = auto()
    EXIT = auto()               #Added for Testing

'''An enumerated list of the available triggers of the Audio Looper'''
class Trigger(Enum):
    PLAY = auto()
    REC = auto()
    PAUSE = auto()
    STOP = auto()
    ADD_TRACK = auto()
    REM_TRACK = auto()
    NEW_TRACK = auto()
    SOLO_TRACK = auto()
    SELECT = auto()
    CLEAR = auto()
    EXIT = auto()


def playLoop(loop, cursor):
    pass

def recordPlay(loop, track, cursor):
    pass

def pauseLoop(loop):
    pass

def stopLoop(loop):
    pass

def recordTrack(loop, cursor, track):
    pass

def loadTrack(loop, track):
    pass

def unloadTrack(loop, track):
    pass

def setMetronome(loop, bpm, timeSigTop, isOn):
    pass

def setTrackFx(track, volume, pan, pitch, isReversed, slip):
    pass

def setLoopFx(loop, volume, pan, pitch, isReversed):
    pass

if __name__ == '__main__':
    rules = {
        State.IDLE: [
            (Trigger.ADD_TRACK, State.LOADED), 
            (Trigger.REC, State.RECORDING),
            (Trigger.EXIT, State.EXIT)
        ],
        State.LOADED: [
            (Trigger.ADD_TRACK, State.LOADED),
            (Trigger.REM_TRACK, State.LOADED), 
            (Trigger.PLAY, State.PLAYING),
            (Trigger.REC, State.PLAYING_AND_RECORDING),
            (Trigger.CLEAR, State.IDLE),
            (Trigger.EXIT, State.EXIT)
        ],
        State.PLAYING: [
            (Trigger.REC, State.PLAYING_AND_RECORDING),
            (Trigger.PAUSE, State.PAUSED),
            (Trigger.STOP, State.LOADED),
            (Trigger.CLEAR, State.IDLE),
            (Trigger.EXIT, State.EXIT)
        ],
        State.PAUSED: [
            (Trigger.ADD_TRACK, State.LOADED),
            (Trigger.REM_TRACK, State.LOADED), 
            (Trigger.PLAY, State.PLAYING),
            (Trigger.REC, State.PLAYING_AND_RECORDING),
            (Trigger.STOP, State.LOADED),
            (Trigger.CLEAR, State.IDLE),
            (Trigger.EXIT, State.EXIT)
        ],
        State.RECORDING: [
            (Trigger.REC, State.PLAYING),
            (Trigger.PLAY, State.PLAYING),
            (Trigger.PAUSE, State.PAUSED),
            (Trigger.STOP, State.LOADED),
            (Trigger.CLEAR, State.IDLE),
            (Trigger.EXIT, State.EXIT)
        ],
        State.PLAYING_AND_RECORDING: [
            (Trigger.REC, State.PLAYING),
            (Trigger.PLAY, State.PLAYING),
            (Trigger.PAUSE, State.PAUSED),
            (Trigger.STOP, State.LOADED),
            (Trigger.CLEAR, State.IDLE),
            (Trigger.EXIT, State.EXIT)
        ],
        State.EXIT: []
    }

    state = State.IDLE

    while state != State.EXIT:
        print(f'The looper is currently in {state}')
        ##Do the stuff you need to do in a given state:
        if(state == State.IDLE):
            pass
        elif(state == State.LOADED):
            pass
        elif(state == State.PLAYING):
            pass
        elif(state == State.PLAYING_AND_RECORDING):
            pass
        elif(state == State.RECORDING):
            pass
        elif(state == State.PAUSED):
            pass

        ##Display options for changing states
        for i in range(len(rules[state])):
            t = rules[state][i][0]
            print(f'{i}: {t}')

        idx = int(input('Select a trigger:'))
        s = rules[state][idx][1]
        state = s

    