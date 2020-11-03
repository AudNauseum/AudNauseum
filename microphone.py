import argparse
import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def microphone():

    try:
            
        device_info = sd.query_devices(1, 'input')
        sample_rate = int(device_info['default_samplerate'])

        file_name = tempfile.mktemp(prefix='mic_recording_',
                                            suffix='.wav', dir='resources/recordings')

        # Make sure the file is opened before recording
        with sf.SoundFile(file_name, mode='x', samplerate=sample_rate,
                        channels=2) as file:
            with sd.InputStream(samplerate=sample_rate, device=1,
                                channels=2, callback=callback):
        
                print('\nRECORDING...\n\npress Ctrl+C to stop the recording\n\n')
        
                while True:
                    file.write(q.get())
                    
    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(file_name))

    return
