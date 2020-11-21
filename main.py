if __name__ == '__main__':
    import sys
    import time
    from audnauseum.state_machine.looper import Looper

    L = Looper()
    L.record()
    time.sleep(5)
    L.stop()
