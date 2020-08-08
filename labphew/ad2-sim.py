import sys
from labphew.core.tools.gui_tools import open_config_dialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Optionally place the path to your default config file here:
default_config = None
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def main(config_file = None):
    """
    Starts the GUI of the Digilent Analog Discovery 2 example.
    Note, if config_file is not specified, or is set to '-default' or '-d', it will fall back to a default file
    specified in this module.
    Note, if '-browse' or '-b' is used for config_file, it will display a window that allows you to browse to the file.
    Note, if no config_file is specified, load_config() of the operator wil be called without

    :param config_file: optional path to config file
    :type config_file: str
    """

    # If -browse (or -b) is used for config_file, display an open file dialog:
    if config_file=='-browse' or config_file=='-b':
        config_file = open_config_dialog()
    # If -default (or -d) is used for config_file, switch it out for the default specified in the top of this file:
    if config_file=='-default' or config_file=='-d':
        config_file = default_config
        print('Using default_config file specified in {}'.format(__name__))
    if config_file is None:
        print('Using Operator without specifying a config file.')

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Load your classes and create your gui:

    # from labphew.controller.digilent.waveforms import DfwController  If you were to use with real device
    from labphew.controller.digilent.waveforms import SimulatedDfwController as DfwController  # To test with simulated device
    from labphew.model.analog_discovery_2_model import Operator
    from labphew.view.analog_discovery_2_view import MonitorWindow, ScanWindow

    instrument = DfwController()
    opr = Operator(instrument)
    opr.load_config()

    # Create a PyQt application
    app = QApplication(sys.argv)
    main_gui = MonitorWindow(opr)
    # To add Scan window(s) to the Monitor window use the following code.
    scan_1 = ScanWindow(opr, parent=main_gui)
    scans = {
        'Sweep &voltage': [scan_1, {'shortcut':"Ctrl+Shift+V", 'statusTip':'Voltage sweep scan'}]  # note that the dictionary is optional
             }
    main_gui.load_scan_guis(scans)
    main_gui.show()  # make sure the GUI will be displayed

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # This line will start the application:
    error_code = app.exec_()
    sys.exit(error_code)


if __name__ == '__main__':
    # When run from command line, this code will pass the command line argument as an argument in the main() function
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()