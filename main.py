if __name__ == '__main__':
    import sys
    import time
    from audnauseum.state_machine.looper import Looper

    L = Looper()
    L.record()
    print("start recording")
    time.sleep(5)
    print("stop recording")
    L.stop()
