from enum import Enum, auto

'''Loop is the primary object that gets passed from state to state'''
class Loop:
    def __init__(self):
        _trackList = None
        _met = Metronome()
        _fx = FxSettings()
    pass

'''Loops manage Tracks. A track is an audio stream and a set of parameters that allow different tracks to sync together'''
class Track:
    _sampleRate = 44100
    _bitDepth = 16
    _bpm = None
    _length_in_beats = None
    _isStereo = False
    pass

'''Metronome is an attribute of a Loop that indicates when Metronome Clicks should play'''
class Metronome:
    _bpm = 0
    _timeSigTop = 4
    _timeSigBottom = 4
    _isOn = False
    pass

'''FxSettings are an attribute of both Tracks and Loops.'''
class FxSettings:
    _volume = 0.5
    _pan = 0.5
    _isReversed = False
    _pitchAdjust = 0
    _slip = 0
    pass
        

class State(Enum):
    IDLE = auto()
    LOADING = auto()
    UNLOADING = auto()
    LOADED = auto()
    PAUSED = auto()
    PLAYING = auto()
    RECORDING = auto()
    PLAYING_AND_RECORDING = auto()
    EXIT = auto()

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


if __name__ == '__main__':
    rules = {
        State.IDLE: [
            (Trigger.ADD_TRACK, State.LOADING), 
            (Trigger.REC, State.RECORDING),
            (Trigger.EXIT, State.EXIT)
        ],
        State.LOADING: [
            (Trigger.SELECT, State.LOADED),
            (Trigger.CLEAR, State.IDLE),
            (Trigger.EXIT, State.EXIT)
        ],
        State.UNLOADING: [
            (Trigger.SELECT, State.LOADED),
            (Trigger.CLEAR, State.IDLE),
            (Trigger.EXIT, State.EXIT)
        ],
        State.LOADED: [
            (Trigger.ADD_TRACK, State.LOADING),
            (Trigger.REM_TRACK, State.UNLOADING), 
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
            (Trigger.ADD_TRACK, State.LOADING),
            (Trigger.REM_TRACK, State.UNLOADING), 
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

        for i in range(len(rules[state])):
            t = rules[state][i][0]
            print(f'{i}: {t}')

        idx = int(input('Select a trigger:'))
        s = rules[state][idx][1]
        state = s

    