"""
* File: Camera.py
* Author: AtD, IlV
* Comments:
* Revision history:
* Date       Author      Description
* -----------------------------------------------------------------
** 070524     AtD/IlV         Initial release
* -----------------------------------------------------------------
*
"""
import cv2
import numpy as np  # Import numpy


class Camera:
    """
    A class to represent a camera capture object.

    Attributes:
        cameraIndex (int): The index of the camera.
        width (int): The width of the camera feed.
        height (int): The height of the camera feed.
        cap (cv2.VideoCapture): OpenCV video capture object.

    Methods:
        init_cap(camera_index, height, width): Initializes the camera capture object.
        set_camera_index(value): Sets the camera index after validation.
        set_width(value): Sets the width of the camera feed after validation.
        set_height(value): Sets the height of the camera feed after validation.
        get_frame_size(): Returns the frame size as a tuple.
    """

    def __init__(self, cameraIndex, width, height):
        """
        Constructs all the necessary attributes for the camera object.

        Parameters:
            cameraIndex (int): The index of the camera.
            width (int): The width of the camera feed.
            height (int): The height of the camera feed.
        """
        self.setCameraIndex(cameraIndex)
        self.setWidth(width)
        self.setHeight(height)

        self.cap = self.initCap(cameraIndex, height, width)

    def initCap(self, cameraIndex, height, width):
        """
        Initializes the camera capture object with specified index, width, and height.

        Parameters:
            cameraIndex (int): The index of the camera.
            height (int): The height to set for the camera feed.
            width (int): The width to set for the camera feed.

        Returns:
            cv2.VideoCapture: The initialized camera capture object.
        """
        cap = cv2.VideoCapture(cameraIndex,cv2.CAP_DSHOW)
        cap.set(3, width)  # cv2.CAP_PROP_FRAME_WIDTH
        cap.set(4, height)  # cv2.CAP_PROP_FRAME_HEIGHT
        return cap

    def setCameraIndex(self, value):
        """
        Validates and sets the camera index.

        Parameters:
            value (int): The index of the camera to be set.
        """
        if value < 0:
            raise ValueError(f"camera index can not be negative -> {value}")
        self.cameraIndex = value

    def setWidth(self, value):
        """
        Validates and sets the width of the camera feed.

        Parameters:
            value (int): The width to be set for the camera feed.
        """
        if value < 0:
            raise ValueError(f"width can not be negative -> {value}")
        self.width = value

    def setHeight(self, value):
        """
        Validates and sets the height of the camera feed.

        Parameters:
            value (int): The height to be set for the camera feed.
        """
        if value < 0:
            raise ValueError(f"height can not be negative -> {value}")
        self.height = value

    def getFrameSize(self):
        """
        Returns the current frame size.

        Returns:
            tuple: The width and height of the camera feed.
        """
        return self.width, self.height

    def capture(self):
        """
           Captures a single frame from the camera feed.

           Returns:
               np.ndarray: The captured frame as a NumPy array, or None if the frame could not be captured.
           """
        ret, frame = self.cap.read()
        return frame

    def stopCapture(self):
        self.cap.release()


if __name__ == "__main__":

    camera = Camera(cameraIndex=0, width=1920, height=1080)
    frame = camera.capture()
    if frame is None:
        print("Frame capture failed")
    else:
        print("Frame captured successfully ")
    camera.stopCapture()
