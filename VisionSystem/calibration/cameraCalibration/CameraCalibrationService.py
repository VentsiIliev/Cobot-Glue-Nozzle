import cv2
import numpy as np
from src.plvision.PLVision import ImageProcessing
from src.plvision.PLVision.Calibration import CameraCalibrator

# Paths to camera calibration data




class CameraCalibrationService:
    STORAGE_PATH = "VisionSystem/calibration/cameraCalibration/storage/calibration_result"

    PERSPECTIVE_MATRIX_PATH = STORAGE_PATH+"/perspectiveTransform.npy"
    CAMERA_TO_ROBOT_MATRIX_PATH = STORAGE_PATH+"/cameraToRobotMatrix.npy"

    def __init__(self, chessboardWidth, chessboardHeight, squareSizeMM, skipFrames,storagePath=None):
        if storagePath is not None:
            self.STORAGE_PATH = storagePath
        self.chessboardWidth = chessboardWidth
        self.chessboardHeight = chessboardHeight
        self.squareSizeMM = squareSizeMM
        self.skipFrames = skipFrames
        self.cameraCalibrator = CameraCalibrator(self.chessboardWidth, self.chessboardHeight, self.squareSizeMM)

    def run(self, image,debug=False):
        message=""
        if debug:
            self.__displayDebugImage(image)

        imageShape = image.shape
        imageWidth = imageShape[1]
        imageHeight = imageShape[0]

        """FIND CORNERS FOR INITIAL PERSPECTIVE TRANSFORM. THIS IS DONE SO THAT WE CAN GET THE CROPPED IMAGE THAT WILL BE USED FOR CAMERA CALIBRATION"""
        result, corners = self.cameraCalibrator.findCorners(image.copy())
        if corners is None:
            message = "Corners not found"
            return False,[],[],message

        bottomLeft, bottomRight, topLeft, topRight = self.sortCorners(corners)
        topLeft = (topLeft[0] - 30, topLeft[1] - 30) #TODO - Remove the hard coded values
        topRight = (topRight[0] + 30, topRight[1] - 30)
        bottomRight = (bottomRight[0] + 30, bottomRight[1] + 30)
        bottomLeft = (bottomLeft[0] - 30, bottomLeft[1] + 30)

        """PREPARE SOURCE POINTS AND DESTINATION POINTS FOR INITIAL PERSPECTIVE TRANSFORM (THE ORDER OF POINTS IS IMPORTANT!)
        """
        src_points = np.array([topLeft, topRight, bottomRight, bottomLeft], dtype='float32')
        dst_points = np.array([   #TODO - Remove the hard coded values
            [0, 0],  # Top-left
            [imageWidth, 0],  # Top-right
            [imageWidth, imageHeight],  # Bottom-right
            [0, imageHeight]  # Bottom-left
        ], dtype='float32')

        perspectiveMatrix = cv2.getPerspectiveTransform(src_points, dst_points)
        croppedImage = cv2.warpPerspective(image, perspectiveMatrix, (imageWidth, imageHeight))

        if debug:
            self.__displayDebugImage(croppedImage)

        """PERFORM THE ACTUAL CAMERA CALIBRATION - GET INTRINSIC AND EXTRINSIC PARAMETERS OF THE CAMERA"""
        result, calibrationData, imageCopy, corners = self.cameraCalibrator.performCameraCalibration(
            croppedImage,
            self.STORAGE_PATH)

        """IF CALIBRATION FAILS, RETURN FALSE AND EMPTY MATRICES FOR PERSPECTIVE TRANSFORM AND CAMERA TO ROBOT TRANSFORMATION"""
        if result is False:
            print("Calibration failed")
            print("corners: ", corners)

            if debug:
                cv2.imwrite("calibration_failed.jpg", croppedImage)
                cv2.imshow("Calibration Failed Image", croppedImage)
                cv2.waitKey(1)

            if corners is not None:
                print("corners len: ", len(corners))
                if len(corners) != 651:
                    message = f"Corners not equal to {self.chessboardWidth*self.chessboardHeight}"
            else:
                message = "Corners not found"
            print(message)
            return False,[],[],message

        print("Calibration successful")
        print("corners len: ", len(corners))

        if debug:
            self.__displayDebugImage(imageCopy)

        """UNDISTORED IMAGE THAT WILL BE USED FOR FINAL PERSPECTIVE TRANSFORM"""
        dst = calibrationData[0]
        mtx = calibrationData[1]
        undistorted = ImageProcessing.undistortImage(image, mtx, dst, imageWidth, imageHeight)
        gray = cv2.cvtColor(undistorted.copy(), cv2.COLOR_BGR2GRAY)

        """FIND CORNERS FOR FINAL PERSPECTIVE TRANSFORM"""
        result, corners = self.cameraCalibrator.findCorners(gray)


        """IF CORNERS NOT FOUND, RETURN FALSE AND EMPTY MATRICES FOR PERSPECTIVE TRANSFORM AND CAMERA TO ROBOT TRANSFORMATION"""
        if not result:
            print("No valid corners detected or the structure of corners is unexpected.")
            message = "No valid corners detected or the structure of corners is unexpected."
            return False,[],[],message

        """PREPARE DESTINATION POINTS AND SOURCE POINTS FOR PERSPECTIVE TRANSFORM (THE ORDER OF POINTS IS IMPORTANT!)
        THIS IS WHY WE NEED TO SORT THE CORNERS TO GET THE CORRECT ORDER OF POINTS"""
        points = corners
        bottomLeft, bottomRight, topLeft, topRight = self.sortCorners(corners)
        sortedCorners = [topLeft, topRight, bottomRight, bottomLeft]
        dst_points = np.array([
            [0, 0],  # Top-left
            [imageWidth, 0],  # Top-right
            [imageWidth, imageHeight],  # Bottom-right
            [0, imageHeight]  # Bottom-left
        ], dtype='float32')

        src_points = np.array([topLeft, topRight, bottomRight, bottomLeft], dtype='float32')

        """COMPUTE PERSPECTIVE TRANSFORM MATRIX AND APPLY IT TO THE UNDISTORTED IMAGE"""
        perspectiveMatrix = self.getWorkAreaMatrix(dst_points, src_points)
        warped_image = cv2.warpPerspective(undistorted, perspectiveMatrix, (imageWidth, imageHeight))

        if debug:
            self.__displayDebugImage(warped_image)

        message = "Calibration successful"
        return True,calibrationData,perspectiveMatrix,message



    def getWorkAreaMatrix(self, dst_points, src_points):
        # Compute perspective transform matrix
        print("Computing perspective transform matrix...")
        # perspectiveMatrix = cv2.getPerspectiveTransform(src_points, dst_points)
        perspectiveMatrix, _ = cv2.findHomography(src_points, dst_points)
        print("Perspective transform matrix computed.")
        # Save the perspective matrix for future use
        print("Saving perspective matrix...")
        np.save(self.PERSPECTIVE_MATRIX_PATH,
                perspectiveMatrix)
        print("Saving perspective")

        return perspectiveMatrix



    def sortCorners(self, corners):
        # Convert corners to a flat list of points for sorting
        points = np.squeeze(corners)
        # Sort points to correctly identify four corners
        topLeft = min(points, key=lambda p: p[0] + p[1])  # Smallest x + y
        topRight = max(points, key=lambda p: p[0] - p[1])  # Largest x - y
        bottomLeft = min(points, key=lambda p: p[0] - p[1])  # Smallest x - y
        bottomRight = max(points, key=lambda p: p[0] + p[1])  # Largest x + y
        return bottomLeft, bottomRight, topLeft, topRight

    def computeCameraToRobotTransformationMatrix(self, camera_pts, robot_pts):
        """
        Computes the homography transformation matrix from camera coordinates to robot coordinates.

        Parameters:
            camera_pts: List of 4 (x, y) tuples in camera coordinates
            robot_pts: List of 4 (X, Y) tuples in robot coordinates

        Returns:
            Homography matrix (3x3) and a function that applies the transformation.
        """
        # Convert points to NumPy array (float32)
        camera_pts = np.array(camera_pts, dtype=np.float32)
        robot_pts = np.array(robot_pts, dtype=np.float32)

        # Compute homography matrix (3x3)
        homography_matrix, _ = cv2.findHomography(camera_pts, robot_pts)
        # homography_matrix = cv2.getPerspectiveTransform(camera_pts, robot_pts)
        return homography_matrix

    def __displayDebugImage(self,image):
        cv2.imshow("Debug", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


