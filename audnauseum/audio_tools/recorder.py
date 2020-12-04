# TODO-create file with python's open() and include buffering argument
# TODO-check for file-creation fail (Line 92)

from datetime import datetime
from time import sleep
import soundfile as sf
import sounddevice as sd
import os
import queue
import threading
from audnauseum.data_models.loop import Loop
from audnauseum.data_models.track import Track

import numpy as np
assert np


class Recorder:
    """Handles recording from input devices to file

    Opens input streams to record incoming audio to a file
    and generates a Track from that data to add to the current
    Loop.
    """
    directory: str
    stream: sd.InputStream
    recording: bool
    previously_recording: bool
    audio_queue: queue.Queue
    current_file: str
    loop: Loop
    input_overflows: int
    thread: threading.Thread
    starting_sample: int

    def __init__(self, loop=None):
        self.directory = 'resources/recordings'
        self.stream = None
        self.create_stream()
        self.recording = self.previously_recording = False
        self.audio_queue = queue.Queue()
        self.current_file = None
        self.last_file = None
        self.loop = loop
        if self.loop is None:
            self.loop = Loop()
        self.input_overflows = 0
        self.thread = None

    def create_stream(self, samplerate=44100):
        """Creates the sounddevice InputStream for recording

        The channels and device are inherited from the respective
        defaults in sd.default
        """
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.InputStream(samplerate=samplerate,
                                     callback=self.audio_callback)
        self.stream.start()

    def after(self, ms, func=None, *args):
        sleep(ms/1000)
        if func:
            return func(*args)

    def audio_callback(self, indata: np.ndarray, frames, time, status: sd.CallbackFlags):
        """This is called (from a separate thread) for each audio block."""
        if status.input_overflow:
            self.input_overflows += 1
        if self.recording:
            self.audio_queue.put(indata.copy())
            self.previously_recording = True
        else:
            if self.previously_recording:
                self.audio_queue.put(None)
                self.previously_recording = False

    def on_rec(self):
        """Begins recording audio from the input stream"""
        self.starting_sample = self.loop.audio_cursor

        self.recording = True
        # create directory if not present
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        now = datetime.now()
        filename = self.directory + '/track_' + \
            now.strftime('%Y%m%d%H%M%S') + '.wav'
        self.current_file = filename

        if self.audio_queue.qsize() != 0:
            print('WARNING: Queue not empty!')
        self.thread = threading.Thread(
            target=self.file_writing_thread,
            kwargs=dict(
                file=filename,
                mode='w',
                samplerate=int(self.stream.samplerate),
                channels=self.stream.channels,
                queue=self.audio_queue,
            ),
        )
        self.thread.start()

    def on_stop(self, *args) -> Track:
        self.recording = False
        self.wait_for_thread()
        track = Track(self.current_file, slip=self.starting_sample)
        self.last_file = self.current_file
        self.current_file = None
        self.starting_sample = 0
        return track

    def wait_for_thread(self):
        self.after(0.1, self._wait_for_thread)

    def _wait_for_thread(self):
        if self.thread.is_alive():
            self.wait_for_thread()
            return
        self.thread.join()

    def close_window(self):
        if self.recording:
            self.on_stop()
        self.destroy()

    def file_writing_thread(self, *, queue, **soundfile_args):
        """Write data from queue to file until *None* is received."""
        with sf.SoundFile(**soundfile_args) as file:
            while True:
                data = queue.get()
                if data is None:
                    break
                file.write(data)

    def get_current_file(self):
        return self.current_file

    def get_last_file(self):
        return self.last_file
