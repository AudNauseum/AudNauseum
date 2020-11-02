from data_models.loop import Loop
from .state import State


class RecordState(State):

    def enter(self, loop: Loop):
        pass

    def run(self, loop: Loop):
        pass

    def exit(self, loop: Loop):
        pass
