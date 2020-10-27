from enum import Enum, auto

'''Loop is the primary object that gets passed from state to state'''
class Loop:
    def __init__(self):
        _trackList = None   #List of Tracks in the loop
        _met = Metronome()
        _fx = FxSettings()
    

'''Loops manage Tracks. A track is an audio stream and a set of 
    parameters that allow different tracks to sync together'''
class Track:
    def __init__(self):
        _fileId = None          #File Identifier (Name maybe?)
        _sampleRate = 44100
        _bitDepth = 16
        _bpm = None
        _length_in_beats = None
        _isStereo = False
    

'''Metronome is an attribute of a Loop that indicates when 
    Metronome Clicks should play'''
class Metronome:
    def __init__(self):
        _bpm = 0                #Beats per Minute
        _timeSigTop = 4         #Beats per Measure
        _metVolume = 0.5
        _countIn = False            #Count in one measure before recording starts
        _isOn = False
    

'''FxSettings are an attribute of both Tracks and Loops.'''
class FxSettings:
    def __init__(self):
        _volume = 0.5
        _pan = 0.5
        _isReversed = False
        _pitchAdjust = 0
        _slip = 0
    
        
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

    