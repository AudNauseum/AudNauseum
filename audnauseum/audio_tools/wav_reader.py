import soundfile as sf
import numpy as np

from typing import List
# import time

from audnauseum.data_models.loop import Loop
from audnauseum.constants import BLOCK_SIZE

MAX_CHANNELS = 2


class WavReader:
    """Reads an arbitrary number of WAV files into iterable numpy array

    Ride the wav's, bro"""

    loop: Loop
    blocksize: int
    sound_files: List[sf.SoundFile]

    def __init__(self, loop: Loop, blocksize=BLOCK_SIZE) -> None:
        """Initialize the WavReader

        The WavReader requires a reference to the current Loop.

        A new instance of WavReader is required each time a Loop is set.
        """
        self.loop = loop
        self.blocksize = blocksize
        self.sound_files = None

    def open_files(self, cursor: int = 0) -> None:
        """Opens WAV files into SoundFile objects

        Opens file handles and reads headers into memory
        based on the current loop
        """
        self.sound_files = [sf.SoundFile(track.file_name)
                            for track in self.loop.tracks]
        for file in self.sound_files:
            file.seek(cursor)

    def open_file(self, file_path: str):
        """Opens a single WAV file into the currently SoundFile objects

        Meant to call while the Looper is actively playing,
        this function can add a new track during playback.
        """
        file = sf.SoundFile(file_path)
        self.sound_files.append(file)

    def close_file(self, file_path):
        """Closes an open file handle when a track is removed during playback

        Called to stop the reading of a track file when the track is
        removed using the UI. File handles are kept open for performance
        and not checked on every read, so this signal closes the necessary
        file.
        """
        for index, file in enumerate(self.sound_files):
            if file.name == file_path:
                file.close()
                del self.sound_files[index]
                break

    def read_to_list(self):
        """Reads multiple SoundFile objects to a list of numpy blocks

        Reads the SoundFile objects block-wise into a list of numpy arrays.

        Returns a list of form:
        [(BLOCK_SIZE, CHANNELS), (BLOCK_SIZE, CHANNELS), ...]
        """
        # Uncomment to time how long this operation takes
        # start = time.perf_counter_ns()
        output_data = []

        for i in range(0, len(self.sound_files)):
            if i == 0:
                self.loop.audio_cursor += self.blocksize
            block: np.ndarray = self.sound_files[i].read(self.blocksize)
            if not block.any():
                # No more blocks to read, reset cursor to the beginning
                self.sound_files[i].seek(0)
                if i == 0:
                    self.loop.audio_cursor = 0
            output_data.append(block)
        # print(f'WavReader.read_to_list: {time.perf_counter_ns() - start}')
        return output_data

    def read_to_3d_array(self):
        """Reads multiple SoundFile objects to a 3d numpy array

        Returns a 3d array of form:
        (BLOCK_SIZE, CHANNELS, X)

        Where X is the number of SoundFile objects read.

        TODO: Implement and see if this is faster than using a list
        """
        # Track stereo and mono channels in order, to ensure that we write to
        # the correct number of rows
        channel_map = np.empty(len(self.sound_files), dtype=int)
        channel_map[0] = 0
        for i in range(1, len(self.sound_files)):
            channel_map[i] = channel_map[i-1] + self.sound_files[i-1].channels
        # print(f'Channel_Map: {channel_map}')
        output_data = np.zeros(
            (self.blocksize, MAX_CHANNELS, len(self.sound_files)))
        for i in range(0, len(self.sound_files)):
            block: np.ndarray = self.sound_files[i].read(self.blocksize)
            # print(f'Block shape')
            # print(block.shape)
            if not block.any():
                # No more blocks to read, reset cursor to the beginning
                self.sound_files[i].seek(0)

            # print(output_data.shape)
            elif(block.shape[0] < self.blocksize):
                print(f'Block Size of last block: {block.shape[0]}')
            output_data[..., i][0:block.shape[0]] = block
            # print(output_data)
        return output_data
