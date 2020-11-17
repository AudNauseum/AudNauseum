import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from audnauseum.state_machine.looper import Looper
from audnauseum.gui.ui import connect_all_inputs, generate_ui

# Create the State Machine
looper = Looper()

# Absolute path to 'looper.ui' file
ui_file = Path(__file__).parent.absolute() / 'gui' / 'looper.ui'

# Create PyQt5 application
app = QApplication(sys.argv)

# Create the UI for the application
ui = generate_ui(ui_file)
connect_all_inputs(ui, looper)
ui.show()
