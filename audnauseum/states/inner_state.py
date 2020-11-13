from data_models.loop import Loop


class InnerState:
    """Base class for State inherited by other classes"""

    def enter(self, loop: Loop):
        """Run setup tasks before entering the state"""
        assert 0, "enter not implemented"

    def run(self, loop: Loop):
        """Run the main action of the state"""
        assert 0, "run not implemented"

    def exit(self, loop: Loop):
        """Run cleanup tasks before exiting the state"""
        assert 0, "exit not implemented"
