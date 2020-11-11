from data_models.loop import Loop
from data_models.track import Track
import unittest


class LoopTest(unittest.TestCase):
    """Test methods for the Loop data model class"""

    def test_empty_message(self):
        """Check the string representation of the Loop with no Tracks"""
        loop = Loop()
        expected = 'Track List is Empty'
        actual = str(loop)
        self.assertEqual(expected, actual)

    def test_append_track(self):
        pass

    def test_non_empty_str(self):
        """Check the string representation of the Loop with Track(s)"""
        loop = Loop()
        track = Track('resources/recordings/Soft_Piano_Music.wav')

        loop.append(track)
        expected = 'Loop:\n=====\nSoft_Piano_Music.wav\n'
        actual = str(loop)
        self.assertEqual(expected, actual)

    def test_delete_track(self):
        pass


if __name__ == '__main__':
    unittest.main()

"""
if __name__ == "__main__":
    # TESTS
    # Create Loop
    loop = Loop()
    # Create Tracks
    t1 = Track('resources/recordings/Soft_Piano_Music.wav')
    t2 = Track('resources/recordings/Soft_Piano_Music.wav')

    # Contact Loop, get response
    loop.solipsize()

    # Add tracks to loop
    loop.append(t1)
    loop.append(t2)

    # print loop details
    print(loop)

    # access the loop's metronome and fx
    print(f'{loop.met}')
    print(f'{loop.fx}')

    # write loop information to ./json/loops
    loop.write_json()

    # remove a track from the loop by file_name
    if loop.remove('resources/recordings/Soft_Piano_Music.wav'):
        print("I removed a thing.")

    print(loop)

    # remove a track from the loop by index
    if loop.pop(0):
        print("I popped a thing.")

    print(loop)

"""
