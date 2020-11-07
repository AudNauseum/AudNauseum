import json
import ntpath
import sys
sys.path.append('data_models')
sys.path.append('metronome')
from metronome import Metronome

from track import Track
from fx_settings import FxSettings
from complex_encoder import ComplexEncoder


class Loop:
    '''Loop is the primary object that gets passed from state to state'''

    def __init__(self):
        self.file_name = None
        self._tracks: list[Track] = []  # List of Tracks in the loop
        self._met = Metronome(100, 4)   # Initializes a metronome
        self._fx = FxSettings()         # Initializes Volume, Pan, Pitch, Reverse, and Slip settings for a loop
        self.audio_cursor = 0           # Sets the audio cursor to point at the beginning of the loop
    
    '''When printing a loop object, I have elected to print the file names of the tracks in the loop. 
    I'm not sure how useful that is, but until I can think of a compelling reason to worry about printing 
    loops--it seems like a reasonable approach, and is sufficient for testing'''
    def __str__(self):
        if(len(self.tracks) == 0):
            return(f'Track List is Empty')
        output = 'Loop:\n=====\n'
        for each in self.tracks:
            output += ntpath.basename(each.file_name) + '\n'
        return(output)
    
    '''Just to test that I can reach a loop object. "I loop therefore I am"'''
    def solipsize(self):
        print(f"I am a Loop object")
    
    @property
    def track_count(self):
        return len(self._tracks)
    
    @property
    def tracks(self):
        return self._tracks
    
    @tracks.setter
    def tracks(self, track):
        try:
            self._tracks = track
        except:
            pass

    '''Add a track to track list'''
    def append(self, val):
        try:
            self._tracks = self._tracks + [val]
            return True
        except:
            return False

    '''Add a list of tracks to track list'''
    def extend(self, val):
        try:
            self._tracks = self.tracks.extend(val)
            return True
        except:
            return False
    '''Remove a track by file_path. Removes the first instance of a Track with a given file_path'''
    def remove(self, file_path):
        for index, track in enumerate(self.tracks):
            if track.file_name == file_path:
                del self.tracks[index]
                return True
        return False
    
    '''Remove a track by index in the tracks list.  Note: Does not return the Track removed from the list. 
    I chose to return a bool to track success.
    If anyone thinks of a good reason to return the object instead of tracking success of the operation, 
    we can do that.'''
    def pop(self, index):
        if(index < len(self.tracks)):
            self.tracks.pop(index)
            return True
        else:
            return False

    @property
    def met(self):
        return self._met
    
    @property
    def fx(self):
        return self._fx

    def reprJSON(self):
        return dict(tracks = self.tracks, met=self.met, fx = self.fx)
    
    def write_json(self):
        if not(self.file_name):
            self.file_name = input('Enter File Name: ')
        with open('./json/loops/' + ntpath.splitext(ntpath.basename(self.file_name))[0] + '.json', 'w') as f:
            f.write(json.dumps(self, cls=ComplexEncoder))
if __name__ == "__main__":
    #TESTS
    #Create Loop
    l = Loop()
    #Create Tracks
    t1=Track(f'resources/recordings/Soft_Piano_Music.wav')
    t2=Track(f'resources/recordings/Soft_Piano_Music.wav')
 
    #Contact Loop, get response
    l.solipsize()
 
    #Add tracks to loop
    l.append(t1)
    l.append(t2)

    #print loop details
    print(l)

    #access the loop's metronome and fx
    print(f'{l.met}')
    print(f'{l.fx}')

    #write loop information to ./json/loops
    l.write_json()

    #remove a track from the loop by file_name
    if l.remove(f'resources/recordings/Soft_Piano_Music.wav'):
        print("I removed a thing.")

    print(l)

    #remove a track from the loop by index
    if l.pop(0):
        print("I popped a thing.")
    
    print(l)