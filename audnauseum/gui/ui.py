from audnauseum.state_machine.looper import Looper, LooperStates
import time
from pathlib import Path


from PyQt5.QtWidgets import QFileDialog, QMessageBox, QListWidget, QListWidgetItem
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
    initialize_lcd_display(ui, looper)
    connect_load_loop(ui, looper)
    connect_save_loop(ui, looper)


# Dictionary for creating unique item names in for-loop modified from source code:
# https://stackoverflow.com/questions/6181935/how-do-you-create-different-variable-names-while-in-a-loop

def update_track_list(ui, looper: Looper):

    track_list = looper.loop.tracks
    item = {}

    ui.listWidget.clear()

    index = 1
    for track in track_list:
        name = track.file_name.split('/')[-1]

        item["item{0}".format(index)] = QListWidgetItem(name)
        ui.listWidget.addItem(item["item{0}".format(index)])
        item["item{0}".format(index)].setText(name)
        index += 1

    # Select row 0 by default to prevent a NoneType error
    ui.listWidget.setCurrentRow(0)
    ui.listWidget.setFocus()


def get_track(ui):

    row = ui.listWidget.currentRow()
    track = ui.listWidget.takeItem(row)

    return track


def connect_transport_control_buttons(ui, looper: Looper):
    """TRANSPORT CONTROLS
    Add listeners to each button in transport controls group
    """
    ui.pushButton_record.clicked.connect(looper.record)
    ui.pushButton_record.clicked.connect(
        lambda: update_track_list(ui, looper))
    ui.pushButton_play.clicked.connect(looper.play)
    ui.pushButton_play.clicked.connect(
        lambda: update_track_list(ui, looper))
    ui.pushButton_stop.clicked.connect(looper.stop)
    ui.pushButton_stop.clicked.connect(
        lambda: update_track_list(ui, looper))

    ui.pushButton_record.clicked.connect(
        lambda: transport_status(ui, looper, 'record'))
    ui.pushButton_play.clicked.connect(
        lambda: transport_status(ui, looper, 'play'))
    ui.pushButton_stop.clicked.connect(
        lambda: transport_status(ui, looper,  ''))


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
    ui.pushButton_reverse.clicked.connect(
        lambda: whichbtn(ui, looper, 'reverse'))
    ui.trackPan.valueChanged.connect(
        lambda: slider_value(ui, looper, 'trackPan'))
    ui.loopPan.valueChanged.connect(
        lambda: slider_value(ui, looper, 'loopPan'))
    ui.trackSlip.valueChanged.connect(
        lambda: slider_value(ui, looper, 'trackSlip'))
    ui.trackVolume.valueChanged.connect(
        lambda: slider_value(ui, looper, 'trackVolume'))
    ui.loopVolume.valueChanged.connect(
        lambda: slider_value(ui, looper, 'loopVolume'))


def connect_metronome_buttons(ui, looper: Looper):
    """METRONOME
    Add listener to toggle metronome on or off
    """
    ui.pushButton_metro_on_off.clicked.connect(
        lambda: whichbtn(ui, looper, 'metro_toggle'))


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


def whichbtn(ui, looper: Looper, _str):

    # print("clicked button is", _str)

    if _str == 'reverse':
        # TODO need function in looper to set reverse
        print('reversed')
    elif _str == 'metro_toggle':
        # TODO need function to turn on metronome
        print('metronome toggled')
        # TODO toggle metronome active status


def slider_value(ui, looper: Looper, _str):

    getValue = -1

    if _str == 'trackPan':
        getValue = ui.trackPan.value()
        # TODO need to send track with value
        # looper.set_pan(getValue)
    elif _str == 'loopPan':
        getValue = ui.loopPan.value()
        looper.set_pan(getValue)
    elif _str == 'trackSlip':
        getValue = ui.trackSlip.value()
        # TODO need function in looper to send value
    elif _str == 'loopSlip':
        getValue = ui.loopSlip.value()
        # TODO need function in looper to send value
    elif _str == 'trackVolume':
        getValue = ui.trackVolume.value()
        # TODO need to send track with value
        # looper.set_volume(getValue)
    elif _str == 'loopVolume':
        getValue = ui.loopVolume.value()
        looper.set_volume(getValue)

    print(f"{_str} value is", str(getValue))


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
        update_track_list(ui, looper)
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
    """Open a file dialog for a user to add a Track to a Loop

    Uses a file dialog to allow a user to make a selection of
    the Track they would like to add to the Loop.
    """

    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_path, _ = QFileDialog.getOpenFileName(
        ui, "Choose a Track to add", "./resources/recordings", "Tracks (*.wav)", options=options)

    if file_path:
        rel_path = get_rel_path(file_path)

        # Check if the same file already exists as a Track in the Loop
        # For simplicity with other functionality, we don't allow duplicate tracks
        if any(track.file_name == rel_path for track in looper.loop.tracks):
            file_name = rel_path.split('/')[-1]
            msg = f'Track {file_name} already exists in this loop.'
            show_popup(ui, msg)
            return False

        looper.add_track(rel_path)
        update_track_list(ui, looper)
        return True

        # The user canceled the add track dialog
    return False


def rem_track(ui, looper: Looper) -> bool:

    if looper.state == LooperStates.LOADED:
        track = get_track(ui)
        rel_path = get_rel_path(track.text())
        looper.remove_track(rel_path)
        return True
    elif looper.state == LooperStates.IDLE:
        show_popup(ui, 'Nothing to remove')
        return False
    else:
        show_popup(ui, 'Must be stopped')
        return False


def get_rel_path(abs_path) -> str:
    # create the relative path for track location
    file_name = abs_path.split('/')[-1]
    rel_path = "resources/recordings/" + file_name

    return rel_path

# Modified from example provided in PyQt5 video:  https://www.youtube.com/watch?v=GkgMTyiLtWk


def show_popup(ui, message):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(message)

    msg.exec_()


def transport_status(ui, looper: Looper, status):

    if not looper.state == LooperStates.IDLE:

        if status == 'record':

            ui.status_indicator.setStyleSheet("""
                                                QPushButton 
                                                {
                                                    color: #333;
                                                    border: 2px solid #555;
                                                    border-radius: 20px;
                                                    border-style: outset;
                                                    background: qradialgradient(
                                                        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                                                        radius: 1.35, stop: 0 #fff, stop: 1 #b12
                                                        );
                                                    padding: 5px;
                                                }
                                                """
                                              )
            ui.status_indicator.setText("REC")

        elif status == 'play':

            ui.status_indicator.setStyleSheet("""
                                                QPushButton 
                                                {
                                                    color: #333;
                                                    border: 2px solid #555;
                                                    border-radius: 20px;
                                                    border-style: outset;
                                                    background: qradialgradient(
                                                        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                                                        radius: 1.35, stop: 0 #fff, stop: 1 #1b2
                                                        );
                                                    padding: 5px;
                                                }
                                                """
                                              )

            ui.status_indicator.setText("PLAY")

        else:

            ui.status_indicator.setStyleSheet("""
                                                QPushButton 
                                                {
                                                    color: #333;
                                                    border: 2px solid #555;
                                                    border-radius: 20px;
                                                    border-style: outset;
                                                    background: qradialgradient(
                                                        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                                                        radius: 1.35, stop: 0 #fff, stop: 1 #ddd
                                                        );
                                                    padding: 5px;
                                                }
                                                """
                                              )

            ui.status_indicator.setText("STOP")
