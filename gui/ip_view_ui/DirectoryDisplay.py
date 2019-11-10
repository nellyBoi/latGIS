"""
Nelly Kane
11.05.2019

Classes to hold containers needed to open directory search, grab directory and place path in display window.
"""
from PyQt5 import QtWidgets
from PyQt5.QtGui import (QStandardItem, QStandardItemModel, QFont)
from PyQt5.QtCore import QSize

import ipview_ui


########################################################################################################################
class DirectoryDisplay(QtWidgets.QTextEdit):
    """
    """
    FONT = QFont("Helvetica", 12)
    START_FOLDER = r'C:\Nelly\IPView\image_containers\data\images'  # TODO remove hard path, for quick debug only.
    EMPTY_DIR_MSG = 'Select Directory'

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        """
        """
        self.ui = ui
        super(DirectoryDisplay, self).__init__()

        self.ui.directory_display.setText(DirectoryDisplay.EMPTY_DIR_MSG)
        self.ui.directory_display.setFont(DirectoryDisplay.FONT)

    ####################################################################################################################
    def directory_dialog_pushed(self):
        """
        """
        directory_string = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder: ',
                                                                      DirectoryDisplay.START_FOLDER,
                                                                      QtWidgets.QFileDialog.ShowDirsOnly)

        self.ui.directory_display.setText(directory_string)
        self.ui.directory_display.setFont(QFont("Helvetica", 8))  # TODO why do we have to drop font size here?

    ####################################################################################################################
    def clear_display(self):
        self.ui.directory_display.setText(DirectoryDisplay.EMPTY_DIR_MSG)
