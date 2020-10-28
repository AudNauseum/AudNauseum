from enum import Enum, auto
from time import sleep
from metronome import Metronome
from loop import Loop, Track, FxSettings

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

    currLoop = Loop()

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

    