import os
import sys
import argparse
import tempfile
import queue

from bullet import Bullet
import sys
sys.path.append('metronome')
sys.path.append('data_models')
from metronome import Metronome
from looper import Looper
from data_models.loop import Loop
from data_models.track import Track
from data_models.fx_settings import FxSettings
from microphone import microphone
import soundfile as sf
import sounddevice as sd
import numpy
assert numpy




def introduction():
    print('\n   _____            .__________')                                            
    print('  /  _  \\  __ __  __| _/\\      \\ _____   __ __  ______ ____  __ __  _____')  
    print(' /  /_\  \|  |  \/ __ | /   |   \\\\__  \ |  |  \/  ___// __ \|  |  \/     \\')
    print('/    |    \\  |  / /_/ |/    |    \\/ __ \\|  |  /\\___ \\ \\ ___/|  |  /  Y Y  \\')
    print('\____|__  /____/\\____ |\\____|__  (____  /____//____  >\\___  >____/|__|_|  /')
    print('        \\/           \\/        \\/     \\/           \\/     \\/            \\/') 


    print("\nWelcome to AudNauseum!")
    print("\nPress Ctrl-C at any time during playback to stop a track\n")


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

def load_track() -> str:
    """Displays a list of files to add to a loop"""
    audio_files = list(os.listdir('resources/recordings'))
    if audio_files:
        cli = Bullet(prompt='Choose an audio file:', choices=audio_files)
        audio_file = cli.launch()
        return audio_file

def idle_menu() -> str:
    """Display controls available in idle state"""
    options = ['add_track', 'record', 'metronome', 'metronome_settings', 'exit']
    cli = Bullet(prompt='Select an action', choices=options)
    selection = cli.launch()
    return selection

def loaded_menu() -> str:
    """Display controls available in loaded state"""
    options = ['exit']
    cli = Bullet(prompt='Select an action', choices=options)
    selection = cli.launch()
    return selection

def recording_menu() -> str:
    """Display controls available in recording state"""
    options = ['exit']
    cli = Bullet(prompt='Select an action', choices=options)
    selection = cli.launch()
    return selection

def playing_menu() -> str:
    """Display controls available in playing state"""
    options = ['exit']
    cli = Bullet(prompt='Select an action', choices=options)
    selection = cli.launch()
    return selection

def playing_and_recording_menu() -> str:
    """Display controls available in playing_and_recording state"""
    options = ['exit']
    cli = Bullet(prompt='Select an action', choices=options)
    selection = cli.launch()
    return selection

def paused_menu() -> str:
    """Display controls available in paused state"""
    options = ['exit']
    cli = Bullet(prompt='Select an action', choices=options)
    selection = cli.launch()
    return selection

def record_menu():
    """Display controls for recording from system line input"""
    microphone()
    return 
        

if __name__ == '__main__':

    m = Looper()

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
                    # sys.exit()
                    continue

        if choice.lower() == 'record':
            
            record_menu()
        # if(m.state == 'idle'):
        #     choice = idle_menu()

        #     if choice.lower() == 'add_track':
        #         #Find File
        #         selection = load_track()
        #         #Create Track
        #         t = Track(f'resources/recordings/' + selection)
        #         #Add Track
        #         if(m.loop.append(t)):
        #             #Change States
        #             m.add_track()

        #     if choice.lower() ==  'record':
        #         pass

        #     if choice.lower() == 'metronome':
        #         pass

        #     if choice.lower() == 'metronome_settings':
        #         pass

        #     if choice.lower() == 'exit':
        #         loop = False

        # if(m.state == 'loaded'):
        #     choice = loaded_menu()

        #     if choice.lower() == 'exit':
        #         loop = False 
    
        # if(m.state == 'recording'):
        #     pass

        # if(m.state == 'playing'):
        #     pass

        # if(m.state == 'playing_and_recording'):
        #     pass

        # if(m.state == 'paused'):
        #     pass
            
    print('\nGoodBye!\n')
