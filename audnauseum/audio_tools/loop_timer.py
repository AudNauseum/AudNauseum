import time
import threading
from audnauseum.data_models.loop import Loop


class Timer():
    def __init__(self, loop):
        self.loop: Loop = loop
        self.tick_counter = 0
        self.tick_ms = loop.blocksize/loop.samplerate*1000
        self.tick_max = loop.ticks
        self.is_running = False

    def start(self):
        self.is_running = True
        self.thread = Thread(target=self.run)
        self.thread.start()

    def run(self):
        while(self.is_running):
            tick_counter += 1
            sleep(self.tick_ms)
            for track in loop.tracks:
                if track.start == tick_counter:
                    if not track.is_released:
                        track.release()
                    else:
                        # TODO
                        # target the soundfile passed to aggregator to seek(0), maybe pass it in from Aggregator when calling run?
                        pass
            self.tick_counter %= self.tick_max

    def stop(self):
        self.is_running = False
        self.thread.join()
