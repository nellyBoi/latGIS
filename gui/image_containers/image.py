"""
:file: image.py
:author: Nelly Kane
:date_originated: 10.23.2019

A module for holding, accessing and manipulating image data.
"""
import ntpath
import os
from enum import Enum

import numpy as np
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import qRgb
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


########################################################################################################################
class NotImplementedException(BaseException):
    """
    Exception raised when a file-read was executed and the conversion to a QImage object is not possible due to an
    unimplemented file-type.
    """
    pass


########################################################################################################################
class FileExt(Enum):
    """
    Class to hold image file-extensions.
    """
    JPEG = 1
    TIF = 2
    PNG = 3


########################################################################################################################
class Image(QImage):
    """
    Class to hold a single image from a file-read or a numpy.array.
    """
    gray_color_table = [qRgb(i, i, i) for i in range(256)]

    ####################################################################################################################
    def __init__(self, array: np.ndarray = None, path: str = None, file_name: str = None, **kwargs):
        """
        :param path: full path to file folder
        :param file_name: name of image file
        :param kwargs: RESERVED
        """
        if array is not None:
            self.__array_to_q_image(im=array)
            self.__name = 'from_array'

        else:
            if path is not None:
                file_name = path + file_name

            # create object with constructor of parent class
            super().__init__(file_name)
            self.__name = ntpath.basename(file_name)

    ####################################################################################################################
    def get_name(self) -> str:
        """
        :return: file name
        """
        return self.__name

    ####################################################################################################################
    def get_pixel_value(self, x: int, y: int) -> tuple:
        """
        :param x: row pixel
        :param y: col pixel
        :return: RGB value for an RBG image, grayscale value for a grayscale image
        """
        val = self.pixel(x, y)
        if self.format() == QImage.Format_ARGB32 or self.format() == QImage.Format_RGB32:
            return QColor(val).getRgb()
        if self.format() == QImage.Format_Indexed8:
            return QColor(val).value()

        raise NotImplementedException

    ####################################################################################################################
    def __array_to_q_image(self, im: np.ndarray, copy=False) -> None:
        """
        A method to convert an underlying numpy array of image data into a QImage object.
        :param im: numpy.ndarray of image data
        :param copy: boolean to copy underlying array
        :return: None
        """
        if im is None:
            self = QImage()

        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                super().__init__(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                self.setColorTable(Image.gray_color_table)
                return
            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    super().__init__(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                    return
                elif im.shape[2] == 4:
                    super().__init__(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                    return

        raise NotImplementedException

    ####################################################################################################################
    @staticmethod
    def __get_file_ext(file_name) -> FileExt:
        """
        :param file_name: file name
        :return:  file extension
        """
        file_ext = os.path.splitext(file_name)[-1]
        file_ext_enum = 0

        if ('jpg' in file_ext) or ('JPG' in file_ext):
            file_ext_enum = FileExt.JPEG

        if ('tif' in file_ext) or ('TIF' in file_ext):
            file_ext_enum = FileExt.TIF

        if ('png' is file_ext) or ('PNG' in file_ext):
            file_ext_enum = FileExt.PNG

        return file_ext_enum


########################################################################################################################
class Window(QWidget):
    """
    Simple application window for rendering an image
    """

    def __init__(self, image: QImage):
        super(Window, self).__init__()

        # image label to display rendering
        self.img_label = QLabel(self)

        pix_map = QPixmap.fromImage(image)

        self.img_label.setPixmap(pix_map)
        self.img_label.setMinimumSize(1, 1)
        self.resize(pix_map.width(), pix_map.height())


########################################################################################################################
if __name__ == '__main__':

    # IMAGE = "data/polarbear.jpg"
    IMAGE = "data/tiger.png"
    import sys

    app = QApplication(sys.argv)

    q_image = Image(file_name=IMAGE)
    if q_image.isNull():
        print('AN ISSUE GETTING THE IMAGE')

    print('Pixel Value: ' + str(q_image.get_pixel_value(x=500, y=400)))

    w = Window(image=q_image)
    w.show()

    sys.exit(app.exec_())
