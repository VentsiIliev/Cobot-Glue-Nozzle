import os
import json
import cv2
import numpy as np
from enum import Enum
import platform

from src.plvision.PLVision import Contouring
from src.plvision.PLVision.Camera import Camera
from src.plvision.PLVision.PID.BrightnessController import BrightnessController
from src.plvision.PLVision import ImageProcessing
from src.plvision.PLVision.arucoModule import *
from VisionSystem.calibration.cameraCalibration.CameraCalibrationService import CameraCalibrationService

# Paths to camera calibration data
# CAMERA_DATA_PATH = "VisionSystem/calibration/cameraCalibration/storage/calibration_result/camera_calibration.npz"
CAMERA_DATA_PATH = os.path.join(os.path.dirname(__file__), 'calibration', 'cameraCalibration', 'storage',
                                'calibration_result', 'camera_calibration.npz')
PERSPECTIVE_MATRIX_PATH = os.path.join(os.path.dirname(__file__), 'calibration', 'cameraCalibration', 'storage',
                                       'calibration_result', 'perspectiveTransform.npy')
CAMERA_TO_ROBOT_MATRIX_PATH = os.path.join(os.path.dirname(__file__), 'calibration', 'cameraCalibration', 'storage',
                                           'calibration_result', 'cameraToRobotMatrix.npy')
CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'config.json')


class SettingsKey(Enum):
    INDEX = "Index"
    WIDTH = "Width"
    HEIGHT = "Height"
    SKIP_FRAMES = "Skip frames"
    THRESHOLD = "Threshold"
    EPSILON = "Epsilon"
    CONTOUR_DETECTION = "Contour detection"
    DRAW_CONTOURS = "Draw contours"


class VisionSystem:
    def __init__(self, configFilePath=None, callback=None):
        # read the config.json file
        data = self.__loadSettings(configFilePath)




        self.frameWidth = data[SettingsKey.WIDTH.value]
        self.frameHeight = data[SettingsKey.HEIGHT.value]
        self.skipFrames = data[SettingsKey.SKIP_FRAMES.value]
        self.thresh = data[SettingsKey.THRESHOLD.value]
        self.epsilon = data[SettingsKey.EPSILON.value]
        self.contourDetection = data[SettingsKey.CONTOUR_DETECTION.value]
        self.drawContours = data[SettingsKey.DRAW_CONTOURS.value]
        self.cameraId = data[SettingsKey.INDEX.value]


        self.camera = Camera(self.cameraId, self.frameWidth, self.frameHeight)
        # Load camera data
        self.isSystemCalibrated = False

        self.__loadPerspectiveMatrix()

        self.__loadCameraCalibrationData()

        self.__loadCameraToRobotMatrix()

        if self.cameraData is None or self.perspectiveMatrix is None or self.cameraToRobotMatrix is None:
            self.isSystemCalibrated = False

        self.callback = callback

        # Extract camera matrix and distortion coefficients
        self.cameraMatrix = self.cameraData['mtx']
        self.cameraDist = self.cameraData['dist']

        self.image = None
        self.rawImage = None
        self.correctedImage = None

        self.brightnessController = BrightnessController(Kp=0.5, Ki=0.1, Kd=0.1, setPoint=144)
        self.adjustment = 0

        self.rawMode = False

    def run(self):
        """
            Captures an image from the camera, processes it to find contours, and sorts them iteratively:
            - First contour is the one with centroid closest to the top-left corner.
            - Subsequent contours are chosen based on proximity to the previous contour's centroid.

            Returns:
            tuple: A tuple containing the contours sorted iteratively and the corrected image.
                   If no contours are found, returns (None, None, None).
        """
        self.image = self.camera.capture()

        if self.skipFrames > 0:
            self.skipFrames -= 1
            if self.callback is not None:
                self.callback(None, None, None)
            return None, None, None

        if self.image is None:
            if self.callback is not None:
                self.callback(None, None, None)
            return None, None, None

        self.rawImage = self.image.copy()

        if self.rawMode:
            print("Raw mode")
            return None, self.rawImage, None

        if self.contourDetection:
            # Process image
            if self.isSystemCalibrated:
                self.correctedImage = self.correctImage(self.image.copy())
            else:
                cv2.putText(self.image, "System is not calibrated", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                            2)
                self.correctedImage = self.image

            # Find contours
            contours = self.findContours(self.correctedImage)
            # filter the contours that are within the work area
            # Approximate contours
            approxContours = self.approxContours(contours)
            # approxContours = contours
            # Filter contours by area
            filteredContours = [cnt for cnt in approxContours if cv2.contourArea(cnt) > 1000]
            # filteredContours = approxContours

            # Calculate centroids
            contours_with_centroids = [
                (cnt, Contouring.calculateCentroid(cnt)) for cnt in filteredContours if
                Contouring.calculateCentroid(cnt) is not None
            ]

            if not contours_with_centroids:
                if self.callback is not None:
                    self.callback(None, self.correctedImage, None)
                return None, self.correctedImage, None

            # Start with the contour closest to the top-left corner (0, 0)
            top_left = (0, 0)
            contours_sorted = []
            current_contour, current_centroid = min(
                contours_with_centroids,
                key=lambda x: ((x[1][0] - top_left[0]) ** 2 + (x[1][1] - top_left[1]) ** 2) ** 0.5
            )
            contours_sorted.append(current_contour)

            # Remove the selected contour explicitly
            contours_with_centroids = [
                (cnt, centroid) for cnt, centroid in contours_with_centroids if not (
                        np.array_equal(cnt, current_contour) and centroid == current_centroid
                )
            ]

            # Iteratively find the next closest contour
            while contours_with_centroids:
                # Find the contour closest to the current centroid
                next_contour, next_centroid = min(
                    contours_with_centroids,
                    key=lambda x: ((x[1][0] - current_centroid[0]) ** 2 + (x[1][1] - current_centroid[1]) ** 2) ** 0.5
                )
                contours_sorted.append(next_contour)

                # Remove the selected contour explicitly by matching both contour and centroid
                contours_with_centroids = [
                    (cnt, centroid) for cnt, centroid in contours_with_centroids if not (
                            np.array_equal(cnt, next_contour) and centroid == next_centroid
                    )
                ]

                # Update the current centroid
                current_centroid = next_centroid

            if self.drawContours:
                cv2.drawContours(self.correctedImage, contours_sorted, -1, (0, 255, 0), 1)

            if self.callback is not None:
                self.callback(contours_sorted, self.correctedImage, None)
            return contours_sorted, self.correctedImage, None

        """APPLY PERSPECTIVE TRANSFORMATION TO THE IMAGE AND RETURN THE RESULTING IMAGE."""
        self.correctedImage = self.correctImage(self.image)

        if self.callback is not None:
            self.callback(None, self.correctedImage, None)
        return None, self.correctedImage, None

    def correctImage(self, imageParam):
        """
        Undistorts and applies perspective correction to the given image.
        """
        imageParam = ImageProcessing.undistortImage(imageParam, self.cameraMatrix, self.cameraDist, self.frameWidth,
                                                    self.frameHeight)
        imageParam = cv2.warpPerspective(imageParam, self.perspectiveMatrix, (self.frameWidth, self.frameHeight))

        return imageParam

    def findContours(self, imageParam):
        """
        Converts an image to grayscale, applies thresholding, and finds contours.
        """
        gray = cv2.cvtColor(imageParam, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, self.thresh, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def approxContours(self, contours):
        """
        Approximates contours using the Ramer-Douglas-Pucker algorithm.
        """
        approx = []
        for cnt in contours:
            epsilon = self.epsilon * cv2.arcLength(cnt, True)
            # epsilon = 0.0009 * cv2.arcLength(cnt, True)
            approx_contour = cv2.approxPolyDP(cnt, epsilon, True)
            approx.append(approx_contour)
        return approx

    def calibrateCamera(self):
        """
            Calibrates the camera using the CameraCalibrationService.

            The function runs the camera calibration service on the current image captured by the camera.

            Parameters:
            None

            Returns:
            None
            """
        enableContourDrawingAfterCalibration = self.drawContours
        if self.drawContours:
            self.drawContours = False

        # TODO remove the hardcoded values for chessboardWidth, chessboardHeight, and squareSizeMM
        cameraCalibrationService = CameraCalibrationService(chessboardWidth=31, chessboardHeight=21, squareSizeMM=25,
                                                            skipFrames=30)
        result, calibrationData, perspectiveMatrix, message = cameraCalibrationService.run(self.rawImage)
        if result:
            self.cameraMatrix = calibrationData[1]
            self.cameraDist = calibrationData[0]
            self.perspectiveMatrix = perspectiveMatrix
        else:
            print("Calibration failed")

        if enableContourDrawingAfterCalibration:
            self.drawContours = True
        return result, message

    def adjustBrightness(self, frame):
        """
        Adjusts the brightness of a frame.

        Parameters
        ----------
        frame : numpy.ndarray
            The frame whose brightness is to be adjusted.

        Returns
        -------
        numpy.ndarray
            The frame with adjusted brightness.
        """
        adjustedFrame = self.brightnessController.adjustBrightness(frame, self.adjustment)
        currentBrightness = self.brightnessController.calculateBrightness(adjustedFrame)
        self.adjustment = self.brightnessController.compute(currentBrightness)
        adjustedFrame = self.brightnessController.adjustBrightness(frame, self.adjustment)
        return adjustedFrame

    def captureImage(self):
        # frame = self.camera.capture()
        # frame = self.correctImage(frame)
        print("Capturing image")
        print("Corrected image shape: ", self.correctedImage.shape)
        return self.correctedImage

    def updateSettings(self, settings: dict):
        """
        Updates the camera settings based on the given dictionary.

        Parameters
        ----------
        settings : dict
            A dictionary containing the camera settings to be updated.

        Returns
        -------
        None
        """
        self.thresh = settings[SettingsKey.THRESHOLD.value]
        self.epsilon = settings[SettingsKey.EPSILON.value]
        self.contourDetection = settings[SettingsKey.CONTOUR_DETECTION.value]
        # self.cameraId = settings[SettingsKey.INDEX.value]
        # self.frameWidth = settings[SettingsKey.WIDTH.value]
        # self.frameHeight = settings[SettingsKey.HEIGHT.value]
        self.skipFrames = settings[SettingsKey.SKIP_FRAMES.value]
        self.drawContours = settings[SettingsKey.DRAW_CONTOURS.value]
        return True, "Settings updated successfully"

    def detectArucoMarkers(self,flip = False):
        self.drawContours = False
        image = self.correctedImage
        if flip:
            image = cv2.flip(image, 1)
        arucoDetector = ArucoDetector(arucoDict=ArucoDictionary.DICT_4X4_250)
        try:
            arucoCorners, arucoIds = arucoDetector.detectAll(image)
        except Exception as e:
            print(e)
            return None, None
        self.drawContours = True
        return arucoCorners, arucoIds, image

    """PRIVATE METHODS SECTION"""

    def __loadCameraToRobotMatrix(self):
        try:
            self.cameraToRobotMatrix = np.load(CAMERA_TO_ROBOT_MATRIX_PATH)
        except FileNotFoundError:
            self.cameraToRobotMatrix = None
            self.isSystemCalibrated = True

    def __loadCameraCalibrationData(self):
        try:
            self.cameraData = np.load(CAMERA_DATA_PATH)
            self.isSystemCalibrated = True
        except FileNotFoundError:
            self.cameraData = None

    def __loadPerspectiveMatrix(self):
        try:
            self.perspectiveMatrix = np.load(PERSPECTIVE_MATRIX_PATH)
            self.isSystemCalibrated = True
        except FileNotFoundError:
            self.perspectiveMatrix = None

    def __loadSettings(self, configFilePath):
        if configFilePath is None:
            configFilePath = CONFIG_FILE_PATH
        with open(configFilePath) as f:
            data = json.load(f)
        return data
