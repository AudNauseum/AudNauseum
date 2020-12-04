from audnauseum.audio_tools.wav_reader import WavReader
from threading import Thread
from queue import Queue
import time

import numpy as np

from audnauseum.data_models.loop import Loop


class Aggregator:
    """Aggregator receives multiple numpy arrays, combines, and applies FX

    The Aggregator requires a reference to the current Loop, the WavReader,
    and the queue that is read by the Player.

    A new instance of Aggregator is required each time a Loop is set.
    """
    loop: Loop
    reader: WavReader
    player_queue: Queue
    thread: Thread
    is_running: bool

    def __init__(self, loop: Loop, player_queue: Queue, reader: WavReader):
        self.loop = loop
        self.player_queue = player_queue
        self.reader = reader
        self.thread = None
        self.is_running = False

    def start(self):
        """Starts the processing of the Aggregator

        Opens file handles and creates a thread to activate
        the Reader and process the read audio data.
        """
        self.reader.open_files()
        self.is_running = True
        self.thread = Thread(target=self.process_audio)
        self.thread.start()

    def stop(self):
        """Stops the processing of the Aggregator

        Ends the processing, closes the thread, and closes
        open file handles.
        """
        self.is_running = False
        self.thread.join()
        self.close_all_file_handles()

    def process_audio(self):
        """Continuously process audio data

        The aggregator will start to continuously process audio data
        from the Reader and pass to the Player until stop() is called.
        """
        while self.is_running:
            input_data = self.reader.read_to_list()
            output_data = self.aggregate_list(input_data)
            if output_data.any():
                self.player_queue.put(output_data)

    def add_track(self, file_path: str, slip: int = 0):
        """Opens a file when a track is added during playback

        Calls the reader to open the specified track that was
        added.
        """
        self.reader.add_track(file_path, slip=slip)

    def remove_track(self, file_path):
        """Closes an open file handle when a track is removed during playback

        Called to stop the reading of a track file when the track is
        removed using the UI. File handles are kept open for performance
        and not checked on every read, so this signal closes the necessary
        file.
        """
        if self.is_running:
            self.reader.close_file(file_path)

    def close_all_file_handles(self):
        """Closes all file handles to tracks

        Called on cleanup to ensure open resources get closed
        """
        self.reader.close_all_files()

    def aggregate_list(self, numpy_arrays) -> np.ndarray:
        """Aggregates a list of numpy arrays into a single numpy array

        The list can contain an arbitrarily large amount of tracks, but in
        practice would be less than 10.

        A list of arrays of shape (BLOCK_SIZE,CHANNELS) are summed together to a
        single array of that shape.
        """
        # Uncomment to time how long this operation takes
        # start = time.perf_counter_ns()
        num_tracks = len(numpy_arrays)
        max_blocksize = self.find_max_blocksize(numpy_arrays)

        # Pre-allocates (malloc) the array under the hood
        output_data: np.ndarray = np.zeros((max_blocksize, 2))

        for block in numpy_arrays:
            if block.shape[0] != max_blocksize:
                padding = np.zeros((max_blocksize - block.shape[0], 2))
                block = np.append(block, padding, 0)
            # Add element-wise in-place to reuse allocated memory
            np.add(output_data, block, output_data)

        np.multiply(output_data, 1. / num_tracks, output_data)
        # print(f'Aggregator.aggregate_list: {time.perf_counter_ns() - start}')
        # print(time.perf_counter_ns() - start)
        return output_data

    def find_max_blocksize(self, numpy_arrays) -> int:
        """Finds the largest blocksize in a list of numpy arrays

        In case the arrays aren't exactly the same size, return
        the size of the largest array.
        """
        max_blocksize = 0
        for block in numpy_arrays:
            block_length = block.shape[0]
            if block_length > max_blocksize:
                max_blocksize = block_length
        return max_blocksize


def aggregate_3d_array(self, numpy_3d_array):
    """Aggregates a 3d array to a summed 2d array

    Aggregates a 3d array of shape (BLOCK_SIZE, CHANNELS, X) into a single
    array of shape (BLOCK_SIZE, CHANNELS).

    (BLOCK_SIZE, CHANNELS, X) --> (BLOCK_SIZE, CHANNELS)
    """
    # Uncomment to time how long this operation takes
    start = time.perf_counter_ns()
    num_tracks = numpy_3d_array.shape[2]
    max_blocksize = self.find_max_blocksize_3d(numpy_3d_array)
    # print(self.find_max_blocksize_3d(numpy_3d_array))

    # Pre-allocates (malloc) the array under the hood
    output_data: np.ndarray = np.zeros((max_blocksize, 2))
    for block in range(numpy_3d_array.shape[-1]):
        current_block_size = numpy_3d_array[..., block].shape[0]
        if current_block_size != max_blocksize:
            padding = np.zeros(
                (max_blocksize - current_block_size, 2))
            numpy_3d_array[..., block] = np.append(
                numpy_3d_array[..., block], padding, 0)
        # Add element-wise in-place to reuse allocated memory
        output_data = np.sum(numpy_3d_array, axis=2)

    np.multiply(output_data, 1. / num_tracks, output_data)
    # print(f'Aggregator.aggregate_list: {time.perf_counter_ns() - start}')

    print(time.perf_counter_ns() - start)
    return output_data


def find_max_blocksize_3d(self, numpy_3d_array) -> int:
    """Finds the largest blocksize in a 3d numpy array

    In case the arrays aren't exactly the same size, return
    the size of the largest array.
    """
    max_blocksize = 0
    for block in range(numpy_3d_array.shape[-1]):
        # print("Numpy block")
        # print(numpy_3d_array[..., block])
        current_block_length = numpy_3d_array[..., block].shape[0]
        if current_block_length > max_blocksize:
            max_blocksize = current_block_length
    return max_blocksize
