from models.loop import Loop
from .state import State


class StateMachine:
    loop: Loop

    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.current_state.run()

    def set_state(self, new_state: State):
        self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter()
        self.current_state.run()
