from audnauseum.state_machine.looper import Looper
import time
from pathlib import Path

from PyQt5 import uic


def generate_ui(ui_file: Path):
    """Generates a PyQt5 UI object from a Path to a .ui file"""
    return uic.loadUi(ui_file)


def connect_all_inputs(ui, looper: Looper):
    """Connects all UI inputs to the looper functions"""
    connect_transport_control_buttons(ui, looper)
    connect_track_control_buttons(ui, looper)
    connect_fx_buttons(ui, looper)
    connect_metronome_buttons(ui, looper)
    connect_volume_dial(ui, looper)
    connect_track_select(ui, looper)
    initialize_lcd_display(ui, looper)


def connect_transport_control_buttons(ui, looper: Looper):
    """TRANSPORT CONTROLS
    Add listeners to each button in transport controls group
    """
    ui.pushButton_record.clicked.connect(looper.record)
    ui.pushButton_play.clicked.connect(looper.play)
    ui.pushButton_stop.clicked.connect(looper.stop)


def connect_track_control_buttons(ui, looper: Looper):
    """TRACK CONTROL
    Add listeners to each button in track controls group
    """
    ui.pushButton_add_track.clicked.connect(lambda: whichbtn('add'))
    ui.pushButton_rem_track.clicked.connect(lambda: whichbtn('remove'))
    ui.pushButton_new_track.clicked.connect(lambda: whichbtn('new'))
    ui.pushButton_solo_track.clicked.connect(lambda: whichbtn('solo'))


def connect_fx_buttons(ui, looper: Looper):
    """EFFECTS (FX)
    Add listeners to each button in effects control group
    """
    ui.pushButton_pan_beats.clicked.connect(lambda: whichbtn('pan'))
    ui.pushButton_pitch.clicked.connect(lambda: whichbtn('pitch'))
    ui.pushButton_slip.clicked.connect(lambda: whichbtn('slip'))
    ui.pushButton_reverse.clicked.connect(lambda: whichbtn('reverse'))


def connect_metronome_buttons(ui, looper: Looper):
    """METRONOME
    Add listener to toggle metronome on or off
    """
    ui.pushButton_metro_on_off.clicked.connect(
        lambda: whichbtn('metro_toggle'))


def connect_volume_dial(ui, looper: Looper):
    """VOLUME
    Add listener for volume control
    """
    ui.dial_volume.valueChanged.connect(lambda: dial_value(ui))


def connect_track_select(ui, looper: Looper):
    """TRACK SELECT
    Add listener to get value of track select
    """
    ui.spinBox_context.valueChanged.connect(lambda: spinbox_value(ui))


def initialize_lcd_display(ui, looper: Looper):
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