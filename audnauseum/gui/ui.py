from audnauseum.state_machine.looper import Looper, LooperStates
import time
from pathlib import Path


from PyQt5.QtWidgets import QFileDialog, QMessageBox, QListWidgetItem
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
    set_loop_vol_slider(ui, looper)


def connect_transport_control_buttons(ui, looper: Looper):
    """TRANSPORT CONTROLS
    Add listeners to each button in transport controls group
    """
    ui.pushButton_record.clicked.connect(looper.record)
    ui.pushButton_play.clicked.connect(looper.play)
    ui.pushButton_stop.clicked.connect(looper.stop)

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

    ui.listWidget.currentRowChanged.connect(
        lambda: set_track_vol_slider(ui, looper))


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
        # print('reversed')
        pass
    elif _str == 'metro_toggle':
        # TODO need function to turn on metronome
        # print('metronome toggled')
        # TODO toggle metronome active status
        pass


def slider_value(ui, looper: Looper, _str):

    sValue = -1

    if _str == 'trackPan':
        sValue = ui.trackPan.value()
        # TODO need to send track with value
        # looper.set_pan(sValue)
    elif _str == 'loopPan':
        sValue = ui.loopPan.value()
        looper.set_pan(sValue)
    elif _str == 'trackSlip':
        sValue = ui.trackSlip.value()
        # TODO need function in looper to send value
    elif _str == 'loopSlip':
        sValue = ui.loopSlip.value()
        # TODO need function in looper to send value
    elif _str == 'trackVolume':

        if ui.listWidget.count() > 0:
            ui.trackVolume.setEnabled(True)
            sValue = ui.trackVolume.value()
            track = get_track(ui, looper)
            looper.track_set_volume(track, sValue)

    elif _str == 'loopVolume':
        sValue = ui.loopVolume.value()
        looper.set_volume(sValue)

    print(f"{_str} value is", str(sValue))


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
    """Opens a file dialog for a user to load a new Loop

    Checks for a compatible state and open a file dialog to
    pick a new loop. Load in the new Tracks if a Loop is chosen
    or return False to indicate the state & loop did not change.
    """

    # For simplicity, only allow loading a new loop from IDLE or LOADED
    # This could be made more flexible in the future - make sure to close
    # all resources (streams, files) if loading a loop during play or record
    if looper.state not in [LooperStates.IDLE, LooperStates.LOADED]:
        msg = 'Please stop the current loop before loading a new loop.'
        show_popup(ui, msg)
        return False

    clear_listview(ui, looper)
    file_path = open_file_dialog(ui)
    if file_path:
        looper.load(file_path)
        set_loop_vol_slider(ui, looper)
        init_track_list(ui, looper)
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


def set_loop_vol_slider(ui, looper: Looper):
    value = looper.get_volume()
    ui.loopVolume.setValue(value)


def set_track_vol_slider(ui, looper: Looper):

    if ui.listWidget.count() > 1:

        track = get_track(ui, looper)
        value = looper.track_get_volume(track)
        ui.trackVolume.setValue(value)


def init_track_list(ui, looper: Looper):

    track_list = looper.get_track_list()

    ui.listWidget.clear()

    for track in track_list:
        file_name = track.file_name.split('/')[-1]
        ui.listWidget.addItem(file_name)


def add_track_to_listview(ui, looper: Looper, file_name):

    ui.listWidget.addItem(file_name)
    ui.trackVolume.setEnabled(True)
    ui.listWidget.setCurrentRow(0)


def rem_track_from_listview(ui, looper: Looper, row_num):

    ui.listWidget.takeItem(row_num)


def clear_listview(ui, looper: Looper):

    while ui.listWidget.count() > 0:

        ui.listWidget.takeItem(ui.listWidget.count() - 1)


def get_track_name(ui) -> str:

    # row = ui.listWidget.currentRow()
    track_name = ui.listWidget.currentItem().text()

    return track_name


def get_track(ui, looper: Looper):
    file_name = get_track_name(ui)
    rel_path = get_rel_path(file_name)
    track = looper.loop.get_track(rel_path)
    return track


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
        file_name = get_file_name(rel_path)
        add_track_to_listview(ui, looper, file_name)
        return True

        # The user canceled the add track dialog
    return False


def rem_track(ui, looper: Looper) -> bool:

    if looper.state == LooperStates.LOADED:
        file_name = get_track_name(ui)
        rel_path = get_rel_path(file_name)
        looper.remove_track(rel_path)
        row = ui.listWidget.currentRow()
        rem_track_from_listview(ui, looper, row)

        if ui.listWidget.count() < 1:
            ui.trackVolume.setEnabled(False)

        return True
    elif looper.state == LooperStates.IDLE:
        show_popup(ui, 'Nothing to remove')
        return False
    else:
        show_popup(ui, 'Must be stopped')
        return False


def get_rel_path(abs_path) -> str:
    # create the relative path for track location
    file_name = get_file_name(abs_path)
    rel_path = "resources/recordings/" + file_name

    return rel_path


# Modified from example provided in PyQt5 video:  https://www.youtube.com/watch?v=GkgMTyiLtWk

def get_file_name(abs_path) -> str:

    file_name = abs_path.split('/')[-1]

    return file_name


def show_popup(ui, message):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(message)

    msg.exec_()


def add_recording_to_track_list(ui, looper: Looper):

    file_name = get_file_name(looper.recorder.get_current_file())
    add_track_to_listview(ui, looper, file_name)


def transport_status(ui, looper: Looper, status):

    if not looper.state == LooperStates.IDLE:

        if status == 'record':

            add_recording_to_track_list(ui, looper)
            ui.trackVolume.setEnabled(False)

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
            ui.trackVolume.setEnabled(True)
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
            ui.trackVolume.setEnabled(True)
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
