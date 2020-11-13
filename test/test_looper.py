import unittest
from audnauseum.state_machine.looper import Looper, LooperStates


class LooperStateTransitionsTest(unittest.TestCase):

    def test_initial_state(self):
        """Tests the initial state of the state machine"""
        looper = Looper()
        self.assertEqual(looper.state, LooperStates.IDLE)

    def test_add_track_from_idle(self):
        """Test the transition from idle to loaded"""
        looper = Looper()
        looper.add_track()
        self.assertEqual(looper.state, LooperStates.LOADED)

    def test_record_from_idle(self):
        """Test the transition from idle to recording"""
        looper = Looper()
        looper.record()
        self.assertEqual(looper.state, LooperStates.RECORDING)

    def test_record_from_loaded(self):
        """Test the transition from loaded to recording"""
        looper = Looper()
        looper.add_track()
        looper.record()
        self.assertEqual(looper.state, LooperStates.PLAYING_AND_RECORDING)

    def test_pause_from_recording(self):
        """Test the transition from recording to paused"""
        looper = Looper()
        looper.record()
        looper.pause()
        self.assertEqual(looper.state, LooperStates.PAUSED)

    # TODO: The rest of the state transitions can be tested
