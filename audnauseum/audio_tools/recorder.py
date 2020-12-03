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
from audnauseum.audio_tools.loop_timer import Timer

import numpy as np
assert np


class Recorder(object):
    def __init__(self, directory=None, loop=None, timer=None):
        self.directory = 'resources/recordings'
        self.stream = None
        self.create_stream()
        self.recording = self.previously_recording = False
        self.audio_q = queue.Queue()
        self.current_file: str
        self.loop = loop
        if(self.loop is None):
            self.loop = Loop()
        self.timer = timer
        self.input_overflows = 0
        self.thread = None
        self.current_tick = 0

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
        if(func):
            return(func(*args))
        else:
            return

    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status.input_overflow:
            self.input_overflows += 1
        if self.recording:
            self.audio_q.put(indata.copy())
            self.previously_recording = True
        else:
            if self.previously_recording:
                self.audio_q.put(None)
                self.previously_recording = False

    def on_rec(self):
        self.current_tick = self.timer.tick_counter

        print(f'Tick at Record press: {current_tick}')
        self.recording = True
        # create directory if not present
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        now = datetime.now()
        filename = self.directory + '/track_' + \
            now.strftime('%Y%m%d%H%M%S') + '.wav'
        self.current_file = None
        self.current_file = filename

        if self.audio_q.qsize() != 0:
            print('WARNING: Queue not empty!')
        self.thread = threading.Thread(
            target=self.file_writing_thread,
            kwargs=dict(
                file=filename,
                mode='w',
                samplerate=int(self.stream.samplerate),
                channels=self.stream.channels,
                q=self.audio_q,
            ),
        )
        self.thread.start()

        # NB: File creation might fail!  For brevity, we don't check for this.

    def on_stop(self, *args):
        self.recording = False
        self.wait_for_thread()
        t = Track(self.current_file, starting_tick=self.current_tick)
        self.current_tick = 0
        print(t.file_name)
        self.loop.append(t)
        print(f'There are: {len(self.loop.tracks)} tracks in loop.')

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

    def file_writing_thread(self, *, q, **soundfile_args):
        """Write data from queue to file until *None* is received."""
        with sf.SoundFile(**soundfile_args) as f:
            while True:
                data = q.get()
                if data is None:
                    break
                f.write(data)
