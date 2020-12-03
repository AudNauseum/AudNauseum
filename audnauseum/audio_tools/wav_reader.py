import soundfile as sf
import numpy as np

from typing import List

import math

from audnauseum.data_models.loop import Loop
from audnauseum.constants import BLOCK_SIZE

MAX_CHANNELS = 2


class ReleaseTimer():
    '''Times the release of files to keep them in sync via a slip value.'''
    total_blocks: int
    loop: Loop
    master_timer: int
    sound_files: List[sf.SoundFile]
    waitlist: List[sf.SoundFile]
    release_list: List[sf.SoundFile]

    def __init__(self, loop, blocksize):
        self.blocksize = blocksize
        self.loop = loop
        self.sound_files = self.get_sound_files()
        self.master_timer = self.get_master_timer()
        self.waitlist = self.generate_waitlist()
        self.release_list = None
        self.release_list = []

    def get_sound_files(self, cursor=0):
        if(len(self.loop.tracks) > 0):
            for track in self.loop.tracks:
                self.sound_files.append(sf.SoundFile(track.file_name))
            for each in self.sound_files:
                each.seek(cursor)
        else:
            self.sound_files = []

    def get_master_timer(self):
        '''Find the longest file, and determine how many blocks it has including
         slipped blocks'''
        loop_length = 0
        for i in range(0, len(self.loop.tracks)):
            current_track_length = self.loop.tracks[i].fx.slip + \
                self.sound_files[i].frames
            if(current_track_length > loop_length):
                loop_length = current_track_length
        return math.ceil(loop_length/self.blocksize)

    def generate_waitlist(self):
        '''create an empty list of len(master_timer)'''
        # waitlist = [None] * self.master_timer
        for i in range(0, len(self.loop.tracks)):
            wait_index = self.loop.tracks[i].fx.slip / self.blocksize
            if(wait_index == 0):
                self.release_list.append(self.sound_files[i])
            else:
                self.insert_waitlist(wait_index, self.sound_files[i])

    def dec_waitlist(self):
        '''reduce the timer by one block, pop the front of the queue to released'''
        current = self.waitlist.pop(0)
        if(len(self.waitlist) == 0):
            self.reset_timer()
        if(current is not None):
            self.release_list.extend(current)

    def reset_timer(self):
        self.sound_files = self.get_sound_files()
        self.master_timer = self.get_master_timer()
        self.waitlist = self.generate_waitlist()

    ###########################################################################
    # HELPER FUNCTIONS
    ###########################################################################
    def insert_waitlist(self, i, sound_file):
        '''insert the soundfile into the wait_list at the given index'''
        if(self.waitlist[i] is not None):
            self.waitlist[i] += [sound_file]
        else:
            self.waitlist[i] = [sound_file]

    def release(self, sound_file):
        '''Appends released tracks to the release_list to feed the WavReader'''
        self.release_list.append(sound_file)


class WavReader:
    """Reads an arbitrary number of WAV files into iterable numpy array

    Ride the wav's, bro"""

    loop: Loop
    blocksize: int
    sound_files: List[sf.SoundFile]
    timer = ReleaseTimer

    def __init__(self, loop: Loop, blocksize=BLOCK_SIZE) -> None:
        """Initialize the WavReader

        The WavReader requires a reference to the current Loop.

        A new instance of WavReader is required each time a Loop is set.
        """
        self.loop = loop
        self.blocksize = blocksize
        self.sound_files = None
        self.timer = ReleaseTimer(self.loop, self.blocksize)

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

        for i in range(0, len(self.timer.release_list)):
            if i == 0:
                self.loop.audio_cursor += self.blocksize
            block: np.ndarray = self.timer.release_list[i].read(self.blocksize)
            if not block.any():
                # No more blocks to read, reset cursor to the beginning
                self.timer.release_list[i].seek(0)
                if i == 0:
                    self.loop.audio_cursor = 0
            output_data.append(block)
            self.timer.dec_waitlist()
        # print(f'WavReader.read_to_list: {time.perf_counter_ns() - start}')
        return output_data
