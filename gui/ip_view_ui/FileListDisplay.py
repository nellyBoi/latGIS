"""
Nelly Kane
11.02.2019

A class to control the 'text_list_display' of IPView.
"""
from PyQt5 import QtWidgets
from PyQt5.QtGui import (QStandardItem, QStandardItemModel, QFont)
from PyQt5.QtCore import (QModelIndex, QPersistentModelIndex)

import ipview_ui


########################################################################################################################
class FileListDisplay(QtWidgets.QListView):
    """

    """
    NO_COMPATIBLE_IMAGE_STR = 'No Compatible Images'

    # settings for text display of selected and unselected lines
    UNSELECTED_FONT = QFont("Helvetica", 12)
    UNSELECTED_FONT.setBold(False)
    SELECTED_FONT = QFont("Helvetica", 14)
    SELECTED_FONT.setBold(True)

    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        """
        """
        self.ui = ui

        super(FileListDisplay, self).__init__()
        self.model = QStandardItemModel()
        self.ui.text_list_display.setModel(self.model)

        # list of QStandardItem, each element represents one text line
        self.q_item_list = []

        self.displayed_item_idx = -1

    ####################################################################################################################
    def load_directory_button_pushed(self) -> None:
        """
        Slot method for loading directory upon load push button.
        """
        self.clear_list_display()

        directory = self.ui.directory_display.toPlainText()
        try:
            files_for_display = self.ui.app_data.load_directory(directory=directory)
        except FileNotFoundError as e:
            print(e)
            return

        if len(files_for_display) == 0:
            item = QStandardItem(FileListDisplay.NO_COMPATIBLE_IMAGE_STR)
            self.model.appendRow(item)

        else:
            for f in files_for_display:  # initialize to UNSELECTED
                item = QStandardItem(f)
                item.setFont(FileListDisplay.UNSELECTED_FONT)
                self.q_item_list.append(item)

                self.model.appendRow(item)  # display to scene

        return

    ####################################################################################################################
    def display_next_item(self) -> None:
        """
        Method to display next item. In effect, will change the settings of the old item back to UNCHECKED and will
        change the settings of the next item to CHECKED.
        """
        if self.displayed_item_idx < len(self.q_item_list) - 1:
            self.q_item_list[self.displayed_item_idx].setFont(FileListDisplay.UNSELECTED_FONT)
            self.displayed_item_idx += 1
            self.q_item_list[self.displayed_item_idx].setFont(FileListDisplay.SELECTED_FONT)

        self.__keep_current_item_in_view()

        return

    ####################################################################################################################
    def display_previous_item(self) -> None:
        """
        Method to display next item. In effect, will change the settings of the old item back to UNCHECKED and will
        change the settings of the previous item to CHECKED.
        """
        if self.displayed_item_idx > 0:
            self.q_item_list[self.displayed_item_idx].setFont(FileListDisplay.UNSELECTED_FONT)
            self.displayed_item_idx -= 1
            self.q_item_list[self.displayed_item_idx].setFont(FileListDisplay.SELECTED_FONT)

        self.__keep_current_item_in_view()

        return

    ####################################################################################################################
    def clear_list_display(self) -> None:
        """
        Method to clear text display.
        """
        self.model.clear()
        self.q_item_list = []
        self.displayed_item_idx = -1

        return

    ####################################################################################################################
    def __keep_current_item_in_view(self) -> None:
        """
        Method to auto-scroll the display box to keep the current item in view.
        """
        index = self.model.indexFromItem(self.q_item_list[self.displayed_item_idx])
        self.ui.text_list_display.scrollTo(index, QtWidgets.QAbstractItemView.EnsureVisible)

        return
