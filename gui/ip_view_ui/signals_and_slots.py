"""
Nelly Kane
11.03.2019

signals_and_slots.py

IPView signals, slots and connections.
"""
from ipview_ui import IPViewWindow

import image as im

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt

import FileListDisplay
import DirectoryDisplay


########################################################################################################################
class Signals:
    """
    """
    def __init__(self, ui: IPViewWindow):
        """
        Instantiation must be the last thing the GUI does.
        :param ui: IPViewWindow object
        """
        self.ui = ui
        self.directory_load_pushed = ui.directory_load_push.clicked
        self.clear_pushed = ui.clear_push_button.clicked
        self.next_button_pushed = ui.next_button.clicked
        self.previous_button_pushed = ui.previous_button.clicked
        self.directory_search_button_pushed = ui.directory_search_push_button.clicked


########################################################################################################################
class Slots:
    """
    """
    def __init__(self, ui: IPViewWindow):
        """
        Instantiation must be the last thing the GUI does.
        :param ui: IPViewWindow object
        """
        self.ui = ui
        self.file_list_display = FileListDisplay.FileListDisplay(ui=ui)
        self.directory_display = DirectoryDisplay.DirectoryDisplay(ui=ui)

    ####################################################################################################################
    def clear_button_pushed(self) -> None:
        """
        Slot method for clearing all data from the UI and from memory.
        """
        # clear event data
        self.ui.app_data.clear_data()

        # clear filename text display
        self.file_list_display.clear_list_display()

        # clear any image from display and reset to blank screen
        scene = QGraphicsScene()
        scene.clear()
        self.ui.image_display.setScene(scene)
        self.ui.image_display.show()
        self.directory_display.clear_display()

        return

    ####################################################################################################################
    def next_button_pushed(self) -> None:
        """
        Slot method for a signal from the next push button.
        """
        image = self.ui.app_data.get_next_image()
        self.__display_image(image=image)
        self.file_list_display.display_next_item()

        return

    ####################################################################################################################
    def previous_button_pushed(self) -> None:
        """
        Slot method for a signal from the previous push button.
        """
        image = self.ui.app_data.get_previous_image()
        self.__display_image(image=image)
        self.file_list_display.display_previous_item()

        return

########################################################################################################################
    def __display_image(self, image: im.Image) -> None:
        """
        """
        x = self.ui.image_display.x()
        y = self.ui.image_display.y()
        w = self.ui.image_display.width()
        h = self.ui.image_display.height()
        scene = QGraphicsScene()

        if image is not None:

            image = image.scaled(w, h, Qt.KeepAspectRatio, Qt.FastTransformation)
            scene.addPixmap(QPixmap.fromImage(image))
            self.ui.image_display.setScene(scene)
            self.ui.image_display.show()


########################################################################################################################
class Connections:
    """
    """
    def __init__(self, ui: IPViewWindow):
        """
        Instantiation must be the last thing the GUI does.
        :param ui: IPViewWindow object
        """
        self.ui = ui
        self.__signals = Signals(ui=self.ui)
        self.__slots = Slots(ui=self.ui)

        # connect signals and slots
        self.__signals.directory_load_pushed.connect(self.__slots.file_list_display.load_directory_button_pushed)
        self.__signals.clear_pushed.connect(self.__slots.clear_button_pushed)
        self.__signals.next_button_pushed.connect(self.__slots.next_button_pushed)
        self.__signals.previous_button_pushed.connect(self.__slots.previous_button_pushed)
        self.__signals.directory_search_button_pushed.connect(self.__slots.directory_display.directory_dialog_pushed)

