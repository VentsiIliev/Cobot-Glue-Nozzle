import numpy as np
import cv2

"""THIS CLASS REPRESENTS THE ROBOT CALIBRATION SERVICE
    IT IS RESPONSIBLE FOR CALIBRATING THE ROBOT USING THE CAMERA POINTS AND ROBOT POINTS
    IT ALSO COMPUTES THE CAMERA TO ROBOT MATRIX AND SAVES IT TO A FILE
    """

CAMERA_TO_ROBOT_MATRIX_PATH = "VisionSystem/calibration/cameraCalibration/storage/calibration_result/cameraToRobotMatrix.npy"
ROBOT_POINTS_PATH = "VisionSystem/calibration/cameraCalibration/storage/calibration_result/robotPoints.txt"
CAMERA_POINTS_PATH = "VisionSystem/calibration/cameraCalibration/storage/calibration_result/cameraPoints.txt"

class RobotCalibrationService():
    def __init__(self):
        self.__cameraPoints = []
        self.__robotPoints = []
        self.cameraToRobotMatrix = None
        self.robotPointIndex = 0
        self.message = ""

        try:
            self.__robotPoints = np.loadtxt(ROBOT_POINTS_PATH).reshape(-1, 3).tolist()
        except (FileNotFoundError, ValueError):
            print("No valid robot points found")
            raise FileNotFoundError("No valid robot points found")

    def calibrate(self):
        print("Calibrating robot...")
        if len(self.__robotPoints) < 3:
            print(f"Error: Not enough robot points. {len(self.__robotPoints)}")
            self.message = f"Error: Not enough robot points. {len(self.__robotPoints)}"
            return False, self.message

        if len(self.__cameraPoints) < 3:
            print(f"Error: Not enough camera points. {len(self.__cameraPoints)}")
            self.message = f"Error: Not enough camera points. {len(self.__cameraPoints)}"
            return False, self.message

        self.__computeMatrix()
        print("Points saved: ", len(self.__robotPoints))

        self.__saveMatrix()

        np.savetxt(ROBOT_POINTS_PATH, np.array(self.__robotPoints), fmt="%.6f")
        np.savetxt(CAMERA_POINTS_PATH, np.array(self.__cameraPoints), fmt="%.6f")

        # Reset points after calibration
        self.__cameraPoints = []
        self.message = "Camera to robot transformation computed successfully"
        return True, self.message


    def __computeMatrix(self):
        print("Computing matrix...")

        # Convert to NumPy arrays (float32)
        camera_pts = np.array(self.__cameraPoints, dtype=np.float32)
        robot_pts = np.array(self.__robotPoints, dtype=np.float32)

        print("Camera points for calib: ", camera_pts)
        print("Robot points for calib: ", robot_pts)

        # Use only (x, y) coordinates for homography
        robotCalibPoints = robot_pts[:, :2]

        # Compute homography matrix (3x3)
        self.cameraToRobotMatrix, _ = cv2.findHomography(camera_pts[:, :2], robotCalibPoints)

    def __saveMatrix(self):
        print("Saving matrix...")
        np.save(CAMERA_TO_ROBOT_MATRIX_PATH, self.cameraToRobotMatrix)

    def setCameraPoints(self, points):
        print(f"Setting camera points... {points}")
        self.__cameraPoints = points

    def setRobotPoints(self, points):
        self.__robotPoints = points

    def getCameraPoints(self):
        return self.__cameraPoints

    def getRobotPoints(self):
        return self.__robotPoints

    def saveRobotPoint(self, point):
        """ Safely append or replace robot points while keeping the z-coordinate intact. """
        if self.robotPointIndex < len(self.__robotPoints):
            self.__robotPoints[self.robotPointIndex] = point
        else:
            self.__robotPoints.append(point)  # Append if index is beyond current list size

        self.robotPointIndex += 1

    def getNextRobotPoint(self):
        """ Ensure safe access to the next robot point """
        if self.robotPointIndex < len(self.__robotPoints):
            return self.__robotPoints[self.robotPointIndex]
        return None  # Return None if out of bounds
