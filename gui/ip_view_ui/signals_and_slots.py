"""
Nelly Kane
11.03.2019

signals_and_slots.py

IPView signals, slots and connections.
"""
import DirectoryDisplay
import FileListDisplay
import ImageDisplay
import SaveImage
import StreamDisplay

from ipview_ui import IPViewWindow


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
        self.save_button_pushed = ui.save_push_button.clicked


########################################################################################################################
class Slots:
    """
    NOTE: Any method defined in here is a slot intended to control multiple functions in the program (i.e. the clear
    may operate on the image display, the directory display and the application data).
    """

    def __init__(self, ui: IPViewWindow):
        """
        Instantiation must be the last thing the GUI does.
        :param ui: IPViewWindow object
        """
        self.ui = ui
        self.file_list_display = FileListDisplay.FileListDisplay(ui=ui)
        self.directory_display = DirectoryDisplay.DirectoryDisplay(ui=ui)
        self.image_display = ImageDisplay.ImageDisplay(ui=ui)
        self.save_image = SaveImage.SaveImage(ui=ui, image_display_object=self.image_display)

        self.stream_display = StreamDisplay.StreamDisplay(ui=self.ui)

    ####################################################################################################################
    def next_button_pushed(self) -> None:
        """
        Slot method for next image called
        """
        self.image_display.next_image()
        self.file_list_display.display_next_item()
        self.stream_display.clear_text()

        return

    ####################################################################################################################
    def previous_button_pushed(self) -> None:
        """
        Slot method for next image called
        """
        self.image_display.previous_image()
        self.file_list_display.display_previous_item()
        self.stream_display.clear_text()

        return

    ####################################################################################################################
    def clear_button_pushed(self) -> None:
        """
        Slot method for clearing all data from the UI and from memory.
        """
        self.ui.app_data.clear_data()
        self.file_list_display.clear_list_display()
        self.image_display.clear_display()
        self.directory_display.clear_display()
        self.stream_display.clear_text()

        return


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
        self.__signals.save_button_pushed.connect(self.__slots.save_image.save_button_pressed)
