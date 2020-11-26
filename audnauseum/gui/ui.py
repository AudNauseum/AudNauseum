from audnauseum.state_machine.looper import Looper
import time
import os
import json
from os import path
from shutil import copyfile
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QMessageBox
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
    initialize_lcd_display(ui, looper)
    connect_load_loop(ui, looper)
    connect_save_loop(ui, looper)


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
    ui.pushButton_add_track.clicked.connect(lambda: add_track(ui, looper))
    ui.pushButton_rem_track.clicked.connect(lambda: rem_track(ui, looper))


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


def initialize_lcd_display(ui, looper: Looper):
    ui.lcdNumber.display(8888)
    # TODO hookup LCD countdown
    # ui.lcdNumber.display(countdown(ui))


def connect_load_loop(ui, looper: Looper):
    """LOAD LOOP
    Add listener for selection of loop JSON file
    """
    ui.pushButton_load_file.clicked.connect(lambda: load_loop(ui, looper))


def connect_save_loop(ui, looper: Looper):
    """SAVE LOOP
    Add listener for save of loop JSON file
    """
    ui.pushButton_save_file.clicked.connect(lambda: save_loop(ui, looper))


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


# Modified from source code example: https://pythonspot.com/pyqt5-file-dialog/

def open_file_dialog(ui) -> str:
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog

    file_path, _ = QFileDialog.getOpenFileName(
        ui, "Choose a loop file", "./resources/json", "Loops Files (*.json)", options=options)

    return file_path


# Modified from source code example: https://pythonspot.com/pyqt5-file-dialog/

def save_file_dialog(ui) -> str:
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog

    file_path, _ = QFileDialog.getSaveFileName(
        ui, "Save loop file as", "./resources/json", "Loops Files (*.json)", options=options)

    return file_path


def load_loop(ui, looper: Looper) -> bool:
    file_path = open_file_dialog(ui)
    if file_path:
        looper.load(file_path)
        return True
    # The user canceled the file dialog
    return False


def save_loop(ui, looper: Looper) -> bool:
    file_path = save_file_dialog(ui)
    if file_path:
        looper.write_loop(file_path)
        return True
    # The user canceled the save dialog
    return False


def add_track(ui, looper: Looper) -> bool:

    # TODO this doesn't do anything really
    if not looper.state == 'IDLE':

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_path, _ = QFileDialog.getOpenFileName(
            ui, "Choose a Track to add", "./resources/recordings", "Tracks (*.wav)", options=options)

        if file_path:
            rel_path = get_rel_path(file_path)
            looper.load_track(rel_path)
            return True

        # The user canceled the add track dialog
        return False
    show_popup(ui)
    return False


def rem_track(ui, looper: Looper) -> bool:

    # TODO this doesn't do anything really
    if not looper.state == 'IDLE':
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            ui, "Choose a Track to remove", "./resources/recordings", "Tracks (*.wav)", options=options)

        if file_path:
            rel_path = get_rel_path(file_path)
            looper.unload_track(rel_path)
            return True

        # The user canceled the add track dialog
        return False
    show_popup(ui)
    return False


def get_rel_path(abs_path) -> str:
    # create the relative path for track location
    file_name = abs_path.split('/')[-1]
    rel_path = "resources/recordings/" + file_name

    return rel_path

# Modified from example provided in PyQt5 video:  https://www.youtube.com/watch?v=GkgMTyiLtWk


def show_popup(ui):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText("A loop must be loaded.")

    msg.exec_()
