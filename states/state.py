class State:
    """Base class for State inherited by other classes"""

    def enter(self):
        """Run setup tasks before entering the state"""
        assert 0, "enter not implemented"

    def run(self):
        """Run the main action of the state"""
        assert 0, "run not implemented"

    def exit(self):
        """Run cleanup tasks before exiting the state"""
        assert 0, "exit not implemented"
