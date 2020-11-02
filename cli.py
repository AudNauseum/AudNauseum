import os
import sys
import argparse
import tempfile
import queue

from bullet import Bullet
from microphone import microphone
import soundfile as sf
import sounddevice as sd
import numpy
assert numpy




def introduction():
    print("Welcome to AudNauseum!")
    print("Press Ctrl-D at any time to exit")


def menu(current_state: str = 'idle') -> str:
    """Displays the main menu for AudNauseum"""
    cli = Bullet(prompt=f'Current state: {current_state}', choices=[
                 "Play", "Record", "Exit"])
    result = cli.launch()
    return result


def play_menu() -> str:
    """Displays a list of recordings to playback"""
    recordings = list(os.listdir('resources/recordings'))
    if recordings:
        cli = Bullet(prompt='Choose a recording:', choices=recordings)
        recording = cli.launch()
        return recording

    print('No sounds to choose from!')
    return ''

def record_menu():
    """Display controls for recording from system line input"""
    microphone()
    return 
        

if __name__ == '__main__':

    loop = True

    introduction()

    while loop:

        choice = menu()
        if choice.lower() == 'play':
            recording = play_menu()
            if recording:
                try:
                    data, fs = sf.read(
                        f'resources/recordings/{recording}', dtype='float32')
                    sd.play(data, fs)
                    status = sd.wait()
                except KeyboardInterrupt:
                    sys.exit()

        if choice.lower() == 'record':
            
            record_menu()

        if choice.lower() == 'exit':
            loop = False
            
        
