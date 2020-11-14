from ..data_models.loop import Loop
from .inner_state import InnerState


class IdleState(InnerState):

    def enter(self, loop: Loop):
        pass

    def run(self, loop: Loop):
        pass

    def exit(self, loop: Loop):
        pass
