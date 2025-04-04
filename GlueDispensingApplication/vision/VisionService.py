import queue

from GlueDispensingApplication import CompareContours
import cv2
import numpy as np
from API.shared.workpiece.WorkpieceService import WorkpieceService
from GlueDispensingApplication.utils import utils, Overlay
from VisionSystem.VisionSystem import VisionSystem
import os
from src.plvision.PLVision.arucoModule import *

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'storage', 'settings', 'camera_settings.json')


class VisionServiceSingleton:
    _visionServiceInstance = None  # Static variable to hold the instance

    @staticmethod
    def get_instance():
        if VisionServiceSingleton._visionServiceInstance is None:
            VisionServiceSingleton._visionServiceInstance = _VisionService()
        return VisionServiceSingleton._visionServiceInstance


class _VisionService(VisionSystem):
    def __init__(self):
        super().__init__(configFilePath=CONFIG_FILE_PATH, callback=None)

        self.MAX_QUEUE_SIZE = 2  # Maximum number of frames to store in the queue
        self.frameQueue = queue.Queue(maxsize=self.MAX_QUEUE_SIZE)
        self.contours = None
        self.drawOverlay = False

    def run(self):
        while True:
            # call super.run

            self.contours, frame, _ = super().run()
            # (self.contours)
            if frame is None:
                continue

            if self.contours is not None:

                # if self.showWorkpieceInfo:
                if self.drawOverlay:
                    workpieceController = WorkpieceService()
                    workpieces = workpieceController.loadAllWorkpieces()
                    cameraToRobotMatrix = self.cameraToRobotMatrix
                    result, newContours = self.processContours()
                    matches, noMatches,_ = CompareContours.findMatchingWorkpieces(workpieces, newContours)
                    ids = []

                    for match in matches:

                        cameraToRobotMatrix = self.cameraToRobotMatrix
                        match.contour = utils.transformToCameraPoints(match.contour, cameraToRobotMatrix)

                        if match.workpieceId not in ids:
                            details = match.getFormattedDetails()
                            Overlay.draw_overlay(frame, details, match.contour)
                            ids.append(match.workpieceId)
                        else:
                            # print("Duplicate ID found in matches")
                            Overlay.drawWorkpieceId(frame, match.contour, match.workpieceId)

                    for noMatch in noMatches:
                        cameraToRobotMatrix = self.cameraToRobotMatrix
                        noMatch = np.array(noMatch, dtype=np.float32)  # Convert noMatch to numpy array
                        noMatch = utils.transformToCameraPoints(noMatch, cameraToRobotMatrix)
                        noMatch = np.array(noMatch, dtype=np.int32).reshape((-1, 1, 2))
                        cv2.drawContours(frame, [noMatch], -1, (0, 0, 255), 1)

            if self.frameQueue.qsize() >= self.MAX_QUEUE_SIZE:
                self.frameQueue.get()  # Remove the oldest frame
            self.frameQueue.put(frame)

    def processContours(self):
        message = ""
        cv2.imwrite("imageDebug.png", self.correctedImage)
        if self.contours is None:
            message = "No contours detected"
            print(message)
            return False, message

        transformedContours = utils.applyTransformation(self.cameraToRobotMatrix,
                                                        self.contours.copy())
        for cnt in transformedContours:
            cnt.append(cnt[0])
        # return as numpy array

        return True,transformedContours

    def getLatestFrame(self):
        if self.frameQueue.empty():
            return None
        frame = self.frameQueue.get_nowait()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return frame

    def getContours(self):
        return self.contours

    def updateCameraSettings(self, settings: dict):
        return self.updateSettings(settings)

    def getFrameWidth(self):
        return self.frameHeight

    def getFrameHeight(self):
        return self.frameWidth

    def getCameraToRobotMatrix(self):
        return self.cameraToRobotMatrix

    def calibrateCamera(self):
        result =  super().calibrateCamera()
        print("Calibration result: ", result)
        return result

    def setRawMode(self, rawMode: bool):
        print("Setting raw mode to: ", rawMode)
        self.rawMode = rawMode

    def detectArucoMarkers(self,flip=False):
        return super().detectArucoMarkers(flip)

    def captureImage(self):
        print("Capturing image")
        image = super().captureImage()
        #print image type
        print("Image type in VisionService: ", type(image))
        print("Corrected image shape: ", image.shape)

        return image

