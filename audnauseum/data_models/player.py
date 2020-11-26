from audnauseum.data_models.track import Track
from audnauseum.data_models.loop import Loop
import sys
import queue
import threading
import time

import soundfile as sf
import sounddevice as sd
import numpy as np
assert np

# TODO: Import from a constants file if used elsewhere in the app?
BLOCK_SIZE = 2048  # roughly 46ms per block given sample rate = 44100
QUEUE_SIZE = 40    # number of blocks in the queue


class Player:
    stream: sd.OutputStream
    file: sf.SoundFile
    playing: bool
    previously_playing: bool
    output_queue: queue.Queue
    blocksize: int
    queue_size: int
    event: threading.Event
    thread: threading.Thread
    loop: Loop
    samplerate: int

    def __init__(self, blocksize=BLOCK_SIZE, queue_size=QUEUE_SIZE):
        self.stream = None
        self.file = None
        self.event = None
        self.playing = False
        self.previously_playing = False
        self.blocksize = blocksize
        self.queue_size = queue_size
        self.output_queue = queue.Queue(maxsize=self.queue_size)
        self.channels = 2

    def play(self, loop: Loop):
        """Starts the streaming playback from file to audio output.

        Currently, this only plays the first Track in the loop,
        but will be modified to play all tracks when we figure out
        how to simultaneously read multiple files into the same
        Numpy array.
        """
        self.loop = loop
        # TODO: Get samplerate at a loop level?
        # Can tracks have different sample rates?
        self.samplerate = loop.tracks[0].samplerate
        # TODO: Change from hard-coded first index to using all in the list
        track = loop.tracks[0]
        self.playing = True
        self.thread = threading.Thread(
            target=self.file_reading_thread, kwargs=dict(track=track))
        self.thread.start()
        self.create_stream()

    def file_reading_thread(self, track: Track, cursor: int = 0):
        """Write data from file to queue."""
        timeout = self.blocksize * self.queue_size / (track.samplerate * 4)
        self.file = sf.SoundFile(track.file_name)
        self.file.seek(cursor)

        while self.playing:
            block: np.ndarray = self.file.read(self.blocksize)
            if not block.any():
                # No more blocks to read, reset cursor to the beginning
                self.file.seek(0)
                continue
            if not self.playing:
                break
            try:
                self.output_queue.put(block, timeout=timeout)
            except queue.Full:
                break

    def create_stream(self):
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.OutputStream(
            blocksize=self.blocksize, dtype='float32',
            samplerate=self.samplerate, channels=self.channels,
            callback=self.callback)
        self.stream.start()

    def stop(self):
        self.playing = False
        self.stream.close()
        self.output_queue.task_done()
        self.file.close()
        self.empty_queue()
        self.thread.join()

    def empty_queue(self):
        """Empty the queue of audio blocks

        Python doesn't seem to actually provide a method to empty a queue
        """
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
                self.output_queue.task_done()
            except queue.Empty:
                pass

    def callback(self, outdata, frames: int, time, status: sd.CallbackFlags):
        """This callback is called from a separate thread by the underlying
        library for each block of audio data.

        The `outdata` must be set to the audio data to play next."""
        if not self.playing:
            raise sd.CallbackAbort
        assert frames == self.blocksize
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        try:
            data: np.ndarray = self.output_queue.get_nowait()
        except queue.Empty as e:
            print('Queue is empty: increase queue_size?', file=sys.stderr)
            raise sd.CallbackAbort from e

        # Check if the audio block isn't full
        if len(data) < len(outdata):
            # zero-byte the remainder of the output in case there's noise
            outdata = np.empty(
                (self.blocksize, self.channels), dtype='float32')
            outdata[:len(data)] = data
        else:
            outdata[:] = data
