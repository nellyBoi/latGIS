"""
file: imagedirectory.py
author: Nelly Kane
date_originated: 10.29.2019

A circular buffer to hold Image objects and image/directory data from a given image directory.

"""
import ntpath
import os
import sys
from enum import Enum

import numpy as np

from image_containers import image as im


########################################################################################################################
class Direction(Enum):
    """
    Enum to hold travel direction of directory read
    """
    FORWARDS = 1
    BACKWARDS = 2


########################################################################################################################
class DirectoryBuffer:
    """
    Class to store buffer_size im.Image objects created externally from a provided directory.
    HOW IT WORKS:
        - Buffer construction will read the first 'buffer_size' compatible files into the buffer, unless the buffer_size
        is 1, then any read waits for the first image to be called.
        - read_index will begin at -1. As 'next_image()' is called 'read_index' will increment by 1 and read a new
        image. If 'previous_image()' is called, 'read_index' will decrement by 1.
        -  buffer indices for reading from the buffer and replacing objects in the buffer is managed internally and the
        object swaps occur in a circular fashion.
        - current object being read will exist in the 'middle' of the buffer from a directory position point of view,
        although it is important to note this is not necessarily the center buffer element since objects will be
        replaced in a circular fashion. The current file being read should always be center of data kept in buffer,
        which is an important thing to keep in mind for logic pertaining to if a new file should be replaced or not.
    """

    ####################################################################################################################
    def __init__(self, directory: str, compatible_files: list, buffer_size: int = 5):
        """

        :param directory:
        :param compatible_files:
        :param buffer_size:
        """
        self.__directory = directory
        self.__compatible_files = compatible_files
        self.__num_files = len(compatible_files)

        # force buffer size to be odd
        if buffer_size % 2 == 0:
            self.__buffer_size = buffer_size - 1
            print('WARNING: Buffer size must be odd, using size: ', + str(self.__buffer_size))
        else:
            self.__buffer_size = buffer_size

        # instantiating buffer data
        self.__data = [None] * self.__buffer_size

        # middle index of buffer
        self.__middle_of_buffer = int((self.__buffer_size - 1) / 2)

        # index creation. buffer indices will pertain to buffer's circular order, file_list indices pertain to indices
        # of compatible_files.
        self.__buffer_read_idx = None
        self.__buffer_replace_idx = None
        self.__file_list_read_idx = None
        self.__file_list_replace_idx = None
        self.__read_direction = None  # used for controlling indices during a direction change
        self.__reset_all_indices()

        self.__initialize_read()

    ####################################################################################################################
    def next_image(self) -> im.Image:
        """
        Method to return the next image object in list of compatible files.
        :return: im.Image object
        """
        if not self.has_next():
            return None

        self.__file_list_read_idx += 1

        # replace object in buffer only if replace-file exists and if the current read is larger than middle-of-buffer
        # index, meaning that buffer should actually be shifted up 1.
        if self.__file_list_read_idx > self.__middle_of_buffer and self.__file_list_replace_idx < (
                self.__num_files - 1) or self.__buffer_size == 1:
            self.__file_list_replace_idx += 1

            if self.__read_direction == Direction.FORWARDS:
                self.__increment_buffer_replace_idx()

            self.__read_direction = Direction.FORWARDS
            self.__push_to_back()

        self.__increment_buffer_read_idx()

        return self.__data[self.__buffer_read_idx]

    ####################################################################################################################
    def previous_image(self) -> im.Image:
        """
        Method to return the next image object in list of compatible files.
        :return: im.Image object
        """
        if not self.has_previous():
            return None

        self.__file_list_read_idx -= 1

        # since we only hold the index of the 'front' of the buffer and a backwards replace needs to occur with files
        # from the back, we define a temp index to represent the file that would be used in the replacement.
        temp_file_read_index = self.__file_list_replace_idx - self.__buffer_size

        # replace object in buffer only if file for replacement exists and if buffer should be shifted down by 1.
        if ((temp_file_read_index >= 0 and (self.__num_files - self.__file_list_read_idx - 1) > self.__middle_of_buffer)
                or self.__buffer_size == 1):
            self.__file_list_replace_idx -= 1

            if self.__read_direction == Direction.BACKWARDS:
                self.__decrement_buffer_replace_idx()

            self.__read_direction = Direction.BACKWARDS
            self.__push_to_front()

        self.__decrement_buffer_read_idx()

        return self.__data[self.__buffer_read_idx]

    ####################################################################################################################
    def has_next(self) -> bool:
        """
        :return: true if another file available, false if not
        """
        return (self.__file_list_read_idx + 1) < self.__num_files

    ####################################################################################################################
    def has_previous(self) -> bool:
        """
        :return: true if previous file available, false if not
        """
        return (self.__file_list_read_idx - 1) >= 0

    ####################################################################################################################
    def clear(self) -> None:
        """
        Method to clear the buffer.
        """
        self.__data = [None] * self.__buffer_size
        self.__reset_all_indices()

        return

    ####################################################################################################################
    def __initialize_read(self) -> None:
        """
        Read the first 'self.__buffer_size' images from directory and store them in buffer.
        """
        self.__read_direction = Direction.FORWARDS

        if self.__buffer_size == 1:
            return

        for idx in np.arange(np.min([self.__buffer_size, self.__num_files])):
            self.__file_list_replace_idx += 1
            self.__increment_buffer_replace_idx()
            self.__push_to_back()

    ####################################################################################################################
    def __push_to_back(self) -> None:
        """
        Note: the '__file_list_replace_idx' remains at the bottom of the directory structure and has been decremented
        but the actual file to create and object with is above it by '__buffer_size' positions.
        """
        filename = os.path.join(self.__directory, self.__compatible_files[self.__file_list_replace_idx])
        self.__data[self.__buffer_replace_idx] = im.Image(file_name=filename)

        return

    ####################################################################################################################
    def __push_to_front(self) -> None:
        """
        Method to push to the front of buffer
        :param image: instance of Image
        """
        filename = os.path.join(self.__directory,
                                self.__compatible_files[self.__file_list_replace_idx - self.__buffer_size + 1])
        self.__data[self.__buffer_replace_idx] = im.Image(file_name=filename)

        return

    ####################################################################################################################
    def __increment_buffer_read_idx(self) -> None:
        """
        Increment index with circular method. For instance, if the buffer_size is 5, the order of the index upon
        incrementation would be [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, ...].
        """
        self.__buffer_read_idx = (self.__buffer_read_idx + 1) % self.__buffer_size
        return

    ####################################################################################################################
    def __decrement_buffer_read_idx(self) -> None:
        """
        Decrement the buffer to read in the reverse order.
        """
        self.__buffer_read_idx = (self.__buffer_read_idx + self.__buffer_size - 1) % self.__buffer_size
        return

    ####################################################################################################################
    def __increment_buffer_replace_idx(self) -> None:
        """
        Increment index with circular method. For instance, if the buffer_size is 5, the order of the index upon
        incrementation would be [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, ...].
        """
        self.__buffer_replace_idx = (self.__buffer_replace_idx + 1) % self.__buffer_size
        return

    ####################################################################################################################
    def __decrement_buffer_replace_idx(self) -> None:
        """
        Decrement the buffer to read in the reverse order.
        """
        self.__buffer_replace_idx = (self.__buffer_replace_idx + self.__buffer_size - 1) % self.__buffer_size
        return

    ####################################################################################################################
    def __reset_all_indices(self) -> None:
        """
        Reset all indices
        """
        self.__buffer_read_idx = -1
        self.__buffer_replace_idx = -1
        self.__file_list_read_idx = -1
        self.__file_list_replace_idx = -1
        self.__read_direction = 0

        return


########################################################################################################################
class ImageDirectory(DirectoryBuffer):
    """
    Class to iterate through a directory both forwards and backwards while skipping files that are incompatible. Images
    are stored in a buffer.
    """
    ALLOWABLE_EXTENSIONS = ['.jpg', '.jpeg', '.JPG', '.png', '.PNG', '.tif', '.TIF']

    ####################################################################################################################
    def __init__(self, directory: str, buffer_size: int = 5):
        """
        :param directory:
        :param buffer_size:
        """
        self.__directory = directory
        self.__buffer_size = buffer_size
        self.__acceptable_files = []
        self.__num_acceptable_files = None

        # get list of compatible files which internally stores in self.__acceptable_files
        self.__allowable_files()

        # call parent constructor on allowable files
        super().__init__(directory=self.__directory, compatible_files=self.__acceptable_files,
                         buffer_size=buffer_size)

    ####################################################################################################################
    def get_list_of_allowable_files(self) -> list:
        """
        :return: list of allowable files
        """
        return self.__acceptable_files

    ####################################################################################################################
    def __allowable_files(self) -> None:
        """
        A method to store files only with extensions defined in ALLOWABLE_EXTENSIONS in a list.
        :return: self.acceptable_files, self_num_files
        """
        all_files = ImageDirectory.list_all_files(path_dir=self.__directory)

        acceptable_files = []
        for current_file in all_files:
            file_ext = os.path.splitext(current_file)[-1]
            if file_ext in ImageDirectory.ALLOWABLE_EXTENSIONS:
                acceptable_files.append(ntpath.basename(current_file))

        self.__acceptable_files = acceptable_files
        self.__num_acceptable_files = len(self.__acceptable_files)

        return

    ####################################################################################################################
    @staticmethod
    def list_all_files(path_dir: str) -> list:
        """
        :param path_dir: path to dir
        :return: list of files in dir
        """
        return [os.path.join(path_dir, f) for f in os.listdir(path_dir) if os.path.isfile(os.path.join(path_dir, f))]


########################################################################################################################
if __name__ == '__main__':

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dir_path = r'data/images'

    image_directory = ImageDirectory(directory=dir_path)

    list_of_windows = []
    while image_directory.has_next():  # test forwards
        image = image_directory.next_image()
        w = im.Window(image=image)
        w.show()
        list_of_windows.append(w)
    while image_directory.has_previous():  # test backwards
        image = image_directory.previous_image()
        w = im.Window(image=image)
        w.show()
        list_of_windows.append(w)

    # show two more forwards
    image = image_directory.next_image()
    w = im.Window(image=image)
    w.show()
    list_of_windows.append(w)
    image = image_directory.next_image()
    w = im.Window(image=image)
    w.show()
    list_of_windows.append(w)

    sys.exit(app.exec_())
