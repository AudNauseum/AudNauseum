from data_models.loop import Loop
from .state import State


class StateMachine:
    """Central class which controls the transition
    between states. Contains a reference to the
    current Loop to pass to the states."""
    loop: Loop

    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.current_state.run()

    def set_state(self, new_state: State):
        self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter()
        self.current_state.run()
