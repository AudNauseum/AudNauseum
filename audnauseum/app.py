import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from audnauseum.state_machine.looper import Looper
from audnauseum.gui.ui import connect_all_inputs, generate_ui

# Create the State Machine
looper = Looper()

# Absolute path to 'looper.ui' file
ui_file = Path(__file__).parent.absolute() / 'gui' / 'looper.ui'

# Create PyQt5 application
app = QApplication(sys.argv)

# Set the desktop icon
# Icon generated from IconsFlow
icon_file = Path(__file__).parent.parent.absolute() / \
    'resources' / 'icon' / 'icon.png'
app.setWindowIcon(QIcon(str(icon_file)))

# Create the UI for the application
ui = generate_ui(ui_file)
connect_all_inputs(ui, looper)
ui.closeEvent = looper.shut_down
ui.show()
