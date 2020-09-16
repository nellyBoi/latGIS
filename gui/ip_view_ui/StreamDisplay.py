"""
Nelly Kane
11.13.2019

Controlling the streaming feature in IPView.
"""
from PyQt5.QtWidgets import QWidget

import ipview_ui


########################################################################################################################
class Singleton:
    """
    A class to emulate a singleton. This class does not operate like a true singleton, which has one and only one
    instance. Instead, each object shares a common data-state which has an identical effect.
    """
    _shared_state = {}

    ####################################################################################################################
    def __init__(self):
        self.__dict__ = self._shared_state


########################################################################################################################
class StreamDisplay(Singleton, QWidget):
    """
    A singleton-like class to control the behavior of the stream display.
    """

    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        Singleton.__init__(self)
        QWidget.__init__(self)

        self.ui = ui

    ####################################################################################################################
    def append_row(self, text_row: str) -> None:
        """
        Method to add row of text to display window.
        :param text_row: str to be appended to display window
        """
        self.ui.stream_display.append(text_row)

        return

    ####################################################################################################################
    def clear_text(self) -> None:
        """
        Method to clear stream display.
        """
        self.ui.stream_display.clear()

        return

    ####################################################################################################################
    def __maintain_scroll_pos(self) -> None:
        pass
