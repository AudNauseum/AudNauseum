import soundfile as sf
import sounddevice as sd
import numpy as np

from typing import List
from queue import Queue

from audnauseum.data_models.loop import Loop
from audnauseum.constants import BLOCK_SIZE


class WavFile:
    """Representation of an open file being read

    Tracks variables necessary to determine when to read blocks from the file.
    """
    sound_file: sf.SoundFile
    slip: int
    finished_reading: bool
    is_slipping: bool

    def __init__(self, sound_file: sf.SoundFile = None, slip: int = 0):
        self.sound_file = sound_file
        self.slip = slip
        self.finished_reading = False
        self.is_slipping = slip > 0

    def __repr__(self):
        return f'{self.sound_file.name}: {self.slip=}, {self.is_slipping=}, {self.finished_reading=}'


class WavReader:
    """Reads an arbitrary number of WAV files into iterable numpy array

    Ride the wav's, bro"""

    loop: Loop
    blocksize: int
    files: List[WavFile]
    tracks_to_add: Queue
    read_cursor: int
    last_block_notifier_queue: Queue

    def __init__(self, loop: Loop, last_block_notifier_queue: Queue, blocksize=BLOCK_SIZE) -> None:
        """Initialize the WavReader

        The WavReader requires a reference to the current Loop.

        A new instance of WavReader is required each time a Loop is set.
        """
        self.loop = loop
        self.blocksize = blocksize
        self.files = []
        self.tracks_to_add = Queue()
        self.last_block_notifier_queue = last_block_notifier_queue
        self.read_cursor = 0

    def open_files(self) -> None:
        """Opens WAV files into SoundFile objects

        Opens file handles and reads headers into memory
        based on the current loop. Sets the audio cursor to the slip value
        """
        self.files = [WavFile(sound_file=sf.SoundFile(track.file_name), slip=track.fx.slip)
                      for track in self.loop.tracks]

        for file in self.files:
            file.sound_file.seek(0)

    def add_track(self, file_path: str, slip: int = 0):
        """Adds a track to be played the next time around the loop

        The track has been added to the Loop, play it from the start
        the next time around.
        """
        file = WavFile(sound_file=sf.SoundFile(file_path), slip=slip)
        self.tracks_to_add.put(file)

    def close_file(self, file_path):
        """Closes an open file handle when a track is removed during playback

        Called to stop the reading of a track file when the track is
        removed using the UI. File handles are kept open for performance
        and not checked on every read, so this signal closes the necessary
        file.
        """
        for index, file in enumerate(self.files):
            if file.sound_file.name == file_path:
                file.sound_file.close()
                del self.files[index]
                break

    def close_all_files(self):
        """Closes all file handles

        Closes all open resources, called upon loading a new loop or
        exiting the program.
        """
        for file in self.files:
            file.sound_file.close()
        self.files = []

    def restart_loop(self):
        """Called to restart the reading of files at the beginning

        Starts the reading of files from the beginning, resets cursors,
        and checks for new files to read from.
        """
        # Any Tracks that were added to the Loop should now be read
        while self.tracks_to_add.qsize() != 0:
            self.files.append(self.tracks_to_add.get())

        # Reset the file to initial state
        for file in self.files:
            file.sound_file.seek(0)
            file.is_slipping = file.slip > 0
            file.finished_reading = False

        self.read_cursor = 0

    def read_to_list(self) -> List[np.ndarray]:
        """Reads multiple SoundFile objects to a list of numpy blocks

        Reads the SoundFile objects block-wise into a list of numpy arrays.

        Returns a list of form:
        [(BLOCK_SIZE, CHANNELS), (BLOCK_SIZE, CHANNELS), ...]
        """
        output_data = []
        is_last_block = False

        for file in self.files:
            # Check if the file is still slipping
            if file.is_slipping and self.read_cursor > file.slip:
                file.is_slipping = False

            if file.finished_reading or file.is_slipping:
                # Nothing to play, send a zero array instead
                block: np.ndarray = np.zeros(
                    (self.blocksize, sd.default.channels[1]))
                output_data.append(block)
            else:
                block: np.ndarray = file.sound_file.read(self.blocksize)
                if not block.any():
                    # No more blocks to read, mark it as done
                    file.finished_reading = True
                output_data.append(block)

        self.read_cursor += self.blocksize

        # Restart the loop if the 'master' track is finished
        # Currently hard-coded to always be the first track
        if self.files[0].finished_reading:
            self.restart_loop()
            is_last_block = True

        self.last_block_notifier_queue.put(is_last_block)
        if is_last_block:
            # Remove an item from the queue if this is the last block
            # The aggregator won't put an item in the queue on the empty (last)
            # block, so remove an item here to keep the queues in sync.
            self.last_block_notifier_queue.get()

        return output_data
