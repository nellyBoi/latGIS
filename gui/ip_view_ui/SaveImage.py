"""
Nelly Kane
11.10.2019

A class to same an image in the current display to a file.

 TODO: add automatic extension.
 TODO: Why does save maintain image size but drop in file size? Data-type?
"""
from PyQt5.QtWidgets import QWidget, QFileDialog

import ImageDisplay
import ipview_ui


########################################################################################################################
class SaveImage(QWidget):
    """
    """

    ####################################################################################################################
    def __init__(self,
                 ui: ipview_ui.IPViewWindow,
                 image_display_object: ImageDisplay.ImageDisplay):
        """
        """
        self.ui = ui
        self.image_display_object = image_display_object
        super(SaveImage, self).__init__()
        self.file_name = None

    ####################################################################################################################
    def save_button_pressed(self) -> None:
        """
        Method to pull up a save-as dialog box and allow the user to save the file in the current image_display.
        """
        current_image = self.image_display_object.get_displayed_image()

        # no action if image is not available
        if current_image is None:
            return

        self.__save_file_dialog()

        if self.file_name is not None:
            current_image.save(self.file_name)

    ####################################################################################################################
    def __save_file_dialog(self):
        options = QFileDialog.Options()
        self.file_name, _ = QFileDialog.getSaveFileName(self, "Save image as", "",
                                                        "All Files (*);;Text Files (*.txt)", options=options)
        if self.file_name:
            print('Saving: ' + str(self.file_name))

    ####################################################################################################################
    def has_image(self):
        """ Returns whether or not the scene contains an image pixmap.
        """
        pass
