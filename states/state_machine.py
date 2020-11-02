from data_models.loop import Loop
from .state import State


class StateMachine:
    """Central class which controls the transition
    between states. Contains a reference to the
    current Loop to pass to the states."""
    loop: Loop
    current_state: State

    def __init__(self, initial_state: State, initial_loop: Loop):
        self.loop = initial_loop
        self.current_state = initial_state
        self.current_state.run(self.loop)

    def set_state(self, new_state: State):
        self.current_state.exit(self.loop)
        self.current_state = new_state
        self.current_state.enter(self.loop)
        self.current_state.run(self.loop)
