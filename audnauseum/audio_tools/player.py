from audnauseum.constants import BLOCK_SIZE, PLAYER_QUEUE_SIZE, SAMPLE_RATE

import sys
import queue

import sounddevice as sd
import numpy as np
assert np


class Player:
    stream: sd.OutputStream
    playing: bool
    previously_playing: bool
    input_queue: queue.Queue
    blocksize: int
    queue_size: int
    samplerate: int
    channels: int

    def __init__(self, blocksize=BLOCK_SIZE, queue_size=PLAYER_QUEUE_SIZE, samplerate=SAMPLE_RATE):
        self.stream = None
        self.playing = False
        self.previously_playing = False
        self.blocksize = blocksize
        self.samplerate = samplerate
        self.input_queue = queue.Queue(maxsize=queue_size)
        self.channels = 2

    def play(self):
        """Starts the streaming playback from input data to audio output.
        """
        self.playing = True
        self.create_stream()

    def create_stream(self):
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.OutputStream(
            blocksize=self.blocksize, dtype='float32', channels=self.channels,
            samplerate=self.samplerate, callback=self.callback)
        self.stream.start()

    def stop(self):
        self.playing = False
        self.stream.close()
        if not self.input_queue.empty():
            self.input_queue.task_done()
        self.empty_queue()

    def empty_queue(self):
        """Empty the queue of audio blocks

        Python doesn't seem to actually provide a method to empty a queue
        """
        while not self.input_queue.empty():
            try:
                self.input_queue.get_nowait()
                self.input_queue.task_done()
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
            data: np.ndarray = self.input_queue.get_nowait()
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
