"""
Nelly Kane
11.05.2019

Classes to hold containers needed to open directory search, grab directory and place path in display window.
"""
import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont

import StreamDisplay
import ipview_ui


########################################################################################################################
class DirectoryDisplay(QtWidgets.QTextEdit):
    """
    """
    FONT = QFont("Helvetica", 12)
    START_FOLDER = os.path.join(os.getcwd(), '..')  # starting one folder up from project folder
    EMPTY_DIR_MSG = 'Select Directory'

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        """
        """
        self.ui = ui
        super(DirectoryDisplay, self).__init__()

        # set default state
        self.ui.directory_display.setText(DirectoryDisplay.EMPTY_DIR_MSG)
        self.ui.directory_display.setFont(DirectoryDisplay.FONT)

        self.stream_display = StreamDisplay.StreamDisplay(ui=self.ui)

        self.__last_opened_directory = DirectoryDisplay.START_FOLDER

    ####################################################################################################################
    def directory_dialog_pushed(self):
        """
        A method to
        """
        directory_string = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder: ',
                                                                      self.__last_opened_directory,
                                                                      QtWidgets.QFileDialog.ShowDirsOnly)

        if directory_string is None or len(directory_string) == 0:
            self.stream_display.append_row('Directory Search Cancelled')
            return

        self.__last_opened_directory = directory_string
        self.ui.directory_display.setText(directory_string)
        self.stream_display.append_row('Directory Found')

        return

    ####################################################################################################################
    def clear_display(self):
        """
        A method to clear the directory display.
        """
        self.ui.directory_display.setText(DirectoryDisplay.EMPTY_DIR_MSG)

        return
