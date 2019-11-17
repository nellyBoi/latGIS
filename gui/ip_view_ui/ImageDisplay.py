"""
Nelly Kane
11.12.2019
"""
from PyQt5.QtCore import (Qt, QRectF)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QGraphicsScene)

import StreamDisplay
import image as im
import ipview_ui


########################################################################################################################
class ImageDisplay(QGraphicsScene):
    """
    A class to control the image display in the IPView GUI.
    """

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow):
        """
        """
        self.ui = ui
        super(ImageDisplay, self).__init__()
        # self.__scene = QGraphicsScene()
        self.ui.image_display.setScene(self)

        # image currently on display
        self.__displayed_image = None

        self.stream_display = StreamDisplay.StreamDisplay(ui=self.ui)

    ####################################################################################################################
    def next_image(self) -> None:
        """
        Method for a signal from the next push button.
        """
        image = self.ui.app_data.get_next_image()
        self.__display_image(image=image)

        return

    ####################################################################################################################
    def previous_image(self) -> None:
        """
        Method for a signal from the previous push button.
        """
        image = self.ui.app_data.get_previous_image()
        self.__display_image(image=image)

        return

    ####################################################################################################################
    def clear_display(self) -> None:
        """
         Method to clear the image display.
        """
        self.clear()
        self.ui.image_display.show()
        self.__displayed_image = None  # reset image held in object.

        return

    ####################################################################################################################
    def get_displayed_image(self) -> im.Image:
        """
        :return: Image currently on display.
        """
        return self.__displayed_image

    ####################################################################################################################
    def mousePressEvent(self, event):
        """
        override method of a mouse click event in QGraphicsView
        """
        if self.__displayed_image is None:
            return

        x = event.scenePos().x()
        y = event.scenePos().y()

        height = self.ui.image_display.sceneRect().height()
        width = self.ui.image_display.sceneRect().width()

        # only print row and col if click within scene
        if x < 0 or x >= width or y < 0 or y >= height:
            return

        self.stream_display.append_row('Pixel: row[{0:.2f}], col[{1:.2f}]'.format(y, x))

        return

    ####################################################################################################################
    def __display_image(self, image: im.Image) -> None:
        """
        """
        if image is not None:
            self.clear()
            self.__displayed_image = image  # set reference to image in object
            self.addPixmap(QPixmap.fromImage(self.__displayed_image))
            self.ui.image_display.setSceneRect(QRectF(self.__displayed_image.rect()))

            # ensures scene rectangle (rect) fits in view port.
            self.ui.image_display.fitInView(self.ui.image_display.sceneRect(), Qt.KeepAspectRatio)
            self.ui.image_display.show()

        return
