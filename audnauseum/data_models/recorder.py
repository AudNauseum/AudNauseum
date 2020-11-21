# TODO-create file with python's open() and include buffering argument
# TODO-check for file-creation fail (Line 92)

import os
import queue
import sys
import tempfile
import threading

import numpy as np
import sounddevice as sd
import soundfile as sf
from time import sleep
from datetime import datetime


class Recorder(object):
    def __init__(self, directory=None, track_counter=0):
        if directory is None:
            now = datetime.now()
            self.directory = 'loop_' + now.strftime('%Y%m%d%H%M%S')
        else:
            self.directory = directory
        self.track_counter = track_counter
        self.stream = None
        self.create_stream()
        self.recording = self.previously_recording = False
        self.audio_q = queue.Queue()

    def create_stream(self, samplerate=44100, device=[0, 1], channels=1):
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.InputStream(samplerate=samplerate,
                                     device=device,
                                     channels=channels,
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
        self.recording = True
        # create directory if not present
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        filename = self.directory + '/track_' + \
            str(self.track_counter).zfill(4) + '.wav'
        self.track_counter += 1

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

    def wait_for_thread(self):
        self.after(10, self._wait_for_thread)

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



def main():
    R = Recorder('loop_test', 5)
    R.on_rec()
    sleep(5)
    R.on_stop()
    print("record next file")
    R.on_rec()
    sleep(5)
    R.on_stop()


if __name__ == '__main__':
    main()
