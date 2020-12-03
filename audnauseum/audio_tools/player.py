from audnauseum.constants import BLOCK_SIZE, PLAYER_QUEUE_SIZE, SAMPLE_RATE
from audnauseum.data_models.loop import Loop

import sys
import queue

import sounddevice as sd
import numpy as np
assert np


class Player:
    """Handles streaming of audio blocks from a queue to output devices


    """
    stream: sd.OutputStream
    playing: bool
    previously_playing: bool
    input_queue: queue.Queue
    last_block_notifier_queue: queue.Queue
    blocksize: int
    queue_size: int
    samplerate: int
    loop: Loop

    def __init__(self, loop: Loop = None, blocksize=BLOCK_SIZE, queue_size=PLAYER_QUEUE_SIZE, samplerate=SAMPLE_RATE):
        self.stream = None
        self.playing = False
        self.previously_playing = False
        self.blocksize = blocksize
        self.samplerate = samplerate
        self.input_queue = queue.Queue(maxsize=queue_size)
        self.last_block_notifier_queue = queue.Queue(maxsize=queue_size)
        self.loop = loop
        if self.loop is None:
            self.loop = Loop()

    def play(self):
        """Starts the streaming playback from input data to audio output.
        """
        self.playing = True
        self.create_stream()

    def create_stream(self):
        """Creates the output stream for audio processing
        """
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.OutputStream(
            blocksize=self.blocksize, dtype='float32',
            samplerate=self.samplerate, callback=self.callback)
        self.stream.start()

    def stop(self):
        """Stops the playback of audio

        Closes the output stream and empties the audio queue
        """
        self.playing = False
        self.stream.close()
        if self.input_queue.qsize() != 0:
            self.input_queue.task_done()
        self.empty_queue()

    def empty_queue(self):
        """Empty the queue of audio blocks

        Python doesn't seem to actually provide a method to empty a queue
        """
        while self.input_queue.qsize() != 0:
            try:
                self.input_queue.get_nowait()
                self.input_queue.task_done()
            except queue.Empty:
                pass
            except ValueError:
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
            is_last_block: bool = self.last_block_notifier_queue.get_nowait()
        except queue.Empty as e:
            print('Queue is empty: increase queue_size?', file=sys.stderr)
            raise sd.CallbackAbort from e

        # Check if the audio block isn't full
        if len(data) < len(outdata):
            # zero-byte the remainder of the output in case there's noise
            outdata = np.empty(
                (self.blocksize, sd.default.channels[1]), dtype='float32')
            outdata[:len(data)] = data
        else:
            outdata[:] = data

        # Update the audio played cursor
        if is_last_block:
            self.loop.audio_cursor = 0
        else:
            self.loop.audio_cursor += frames
