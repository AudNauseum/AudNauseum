import sys
import time
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic

# Absolute path to 'looper.ui' file
ui_file = Path(__file__).parent.absolute() / 'looper.ui'

app = QApplication(sys.argv)

ui = uic.loadUi(ui_file)
ui.show()

# TRANSPORT CONTROLS - Add listeners to each button in transport controls group
ui.pushButton_record.clicked.connect(lambda: whichbtn('record'))
ui.pushButton_play.clicked.connect(lambda: whichbtn('play'))
ui.pushButton_stop.clicked.connect(lambda: whichbtn('stop'))

# TRACK CONTROL - Add listeners to each button in track controls group
ui.pushButton_add_track.clicked.connect(lambda: whichbtn('add'))
ui.pushButton_rem_track.clicked.connect(lambda: whichbtn('remove'))
ui.pushButton_new_track.clicked.connect(lambda: whichbtn('new'))
ui.pushButton_solo_track.clicked.connect(lambda: whichbtn('solo'))

# EFFECTS (FX) - Add listeners to each button in effects control group
ui.pushButton_pan_beats.clicked.connect(lambda: whichbtn('pan'))
ui.pushButton_pitch.clicked.connect(lambda: whichbtn('pitch'))
ui.pushButton_slip.clicked.connect(lambda: whichbtn('slip'))
ui.pushButton_reverse.clicked.connect(lambda: whichbtn('reverse'))

# METRONOME - Add listener to toggle metronome on or off
ui.pushButton_metro_on_off.clicked.connect(
    lambda: whichbtn('metro_toggle'))

# VOLUME - Add listener for volume control
ui.dial_volume.valueChanged.connect(lambda: dial_value(ui))

# TRACK SELECT - Add listener to get value of track select
ui.spinBox_context.valueChanged.connect(lambda: spinbox_value(ui))

ui.lcdNumber.display(8888)
# TODO hookup LCD countdown
# ui.lcdNumber.display(countdown(ui))


def whichbtn(_str):
    print("clicked button is", _str)


def dial_value(ui):
    getValue = ui.dial_volume.value()
    print("volume value is", str(getValue))


def spinbox_value(ui):
    getValue = ui.spinBox_context.value()
    print("track selected is", str(getValue))


def countdown(ui):
    for i in range(1, 1000):
        time.sleep(1)
        return i
