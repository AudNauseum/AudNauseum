import numpy as np
import sounddevice
import time

fs = 44100 # Hz
T = 1. # second, arbitrary length of tone

# 1 kHz sine wave, 1 second long, sampled at 44.1 kHz
t = np.arange(0, T, 1/fs)

x = 0.5 * np.sin(2*np.pi*440*t)   # 0.5 is arbitrary to avoid clipping sound card DAC
x  = (x*32768).astype(np.int16)  # scale to int16 for sound card, converts values between -1 & 1 to values between -32768 & 32768

y = 0.5 * np.sin(2*np.pi*600*t)   # 0.5 is arbitrary to avoid clipping sound card DAC
y  = (y*32768).astype(np.int16)  # scale to int16 for sound card

sounddevice.play(x, fs)  # releases GIL (Global Interpreter Lock - I had to look that up)
time.sleep(1.5)  # NOTE: Since sound playback is async, allow sound playback to finish before Python exits

sounddevice.play(y, fs)
time.sleep(1.5)

#determine which signal is longer, copy it and add the other signal to it element-wise
if len(x) < len(y):
    longer = y.copy()
    longer[:len(x)] += x
else:
    longer = x.copy()
    longer[:len(y)] += y

sounddevice.play(longer, fs)
time.sleep(1.5)