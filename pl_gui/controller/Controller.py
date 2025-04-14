import time

from API.Request import Request
from API.Response import Response
from API import Constants
from API.shared.settings.conreateSettings.CameraSettings import CameraSettings
from API.shared.settings.conreateSettings.RobotSettings import RobotSettings

GET_SETTINGS_TOPIC = "settings/get"
START_TOPIC = "start"

CREATE_WORKPIECE_TOPIC = "createworkpiece"
CALIBRATE_TOPIC = "calibrate"
MANUAL_MOVE_TOPIC = "robot/control/manual"
SAVE_ROBOT_CALIBRATION_POINT = "robot/control/manual/save"
JOG_ROBOT_TOPIC = "robot/control/manual/jog/"
HOME_ROBOT_TOPIC = "robot/control/home"
STOP_ROBOT_TOPIC = "robot/control/stop"
UPDATE_CAMERA_FEED = "cameraFeed/update"

class Controller:
    def __init__(self, requestSender):
        self.requestSender = requestSender

    def sendRequest(self, message):
        if message == GET_SETTINGS_TOPIC:
            return self.__getSettings()
        elif message == START_TOPIC:
            return self.__start()

        elif message == CREATE_WORKPIECE_TOPIC:
            return self.__createWorkpice()
        elif message == CALIBRATE_TOPIC:
            return self.__calibrate()
        elif message == MANUAL_MOVE_TOPIC:
            return self.__manualMove()
        elif message == UPDATE_CAMERA_FEED:
            self.updateCameraFeed()
        elif message == SAVE_ROBOT_CALIBRATION_POINT:
            self.saveRobotCalibrationPoint()
        elif JOG_ROBOT_TOPIC in message:
            self.sendJogRequest(message)
        elif message == HOME_ROBOT_TOPIC:
            self.homeRobot()
        elif message == STOP_ROBOT_TOPIC:
            return self.__stop()
        else:
            self.requestSender.sendRequest(message)

    def __stop(self):
        request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.ACTION_STOP, Constants.REQUEST_RESOURCE_ROBOT)
        self.requestSender.sendRequest(request)

    def homeRobot(self):
        request = Request(Constants.REQUEST_TYPE_EXECUTE,Constants.HOME_ROBOT,Constants.REQUEST_RESOURCE_ROBOT)
        self.requestSender.sendRequest(request)

    def __getSettings(self):
        robotSettingsRequest = Request(Constants.REQUEST_TYPE_GET, Constants.ACTION_GET_SETTINGS,
                                       Constants.REQUEST_RESOURCE_ROBOT)

        cameraSettingsRequest = Request(Constants.REQUEST_TYPE_GET, Constants.ACTION_GET_SETTINGS,
                                        Constants.REQUEST_RESOURCE_CAMERA)

        # contourSettingsRequest = # TODO

        robotSettingsResponseDict = self.requestSender.sendRequest(robotSettingsRequest)
        robotSettingsResponse = Response.from_dict(robotSettingsResponseDict)

        cameraSettingsResponseDict = self.requestSender.sendRequest(cameraSettingsRequest)
        cameraSettingsResponse = Response.from_dict(cameraSettingsResponseDict)

        robotSettingsDict = robotSettingsResponse.data if robotSettingsResponse.status == Constants.RESPONSE_STATUS_SUCCESS else {}
        cameraSettingsDict = cameraSettingsResponse.data if cameraSettingsResponse.status == Constants.RESPONSE_STATUS_SUCCESS else {}

        cameraSettings = CameraSettings(data=cameraSettingsDict)
        robotSettings = RobotSettings(data = robotSettingsDict)

        return cameraSettings,robotSettings

    def __start(self):
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE, action=Constants.ACTION_START)
        responseDict = self.requestSender.sendRequest(request)
        response = Response.from_dict(responseDict)

        if response.status == Constants.RESPONSE_STATUS_ERROR:
            print("Error starting")
            # TODO SHOW ERROR WINDOW

        pass



    def __createWorkpice(self):
        request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.ACTION_CREATE_WORKPIECE)
        responseDict = self.requestSender.sendRequest(request)
        response = Response.from_dict(responseDict)

        if response.status == Constants.RESPONSE_STATUS_ERROR:
            print("Error creating workpiece")
            print(response.message)
            return False,None

        responseData = response.data



        frame = responseData['image']

        return True,responseData

    def saveWorkpiece(self,data):
        request = Request(Constants.REQUEST_TYPE_POST, Constants.ACTION_SAVE_WORKPIECE,
                          Constants.REQUEST_RESOURCE_WORKPIECE, data=data)
        responseDict = self.requestSender.sendRequest(request)
        response = Response.from_dict(responseDict)

        if response.status == Constants.RESPONSE_STATUS_ERROR:
            message = "Error saving workpiece"
            return False, response.message

        return True, response.message

    def __calibrate(self):
        from PyQt6.QtWidgets import QMessageBox
        request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.CAMERA_ACTION_RAW_MODE_ON,
                          Constants.REQUEST_RESOURCE_CAMERA)
        response = self.requestSender.sendRequest(request)
        response = Response.from_dict(response)

        if response.status == Constants.RESPONSE_STATUS_ERROR:
            # show message dialog
            msg = QMessageBox()
            msg.setWindowTitle("Calibration Failed")
            msg.setText("Error entering raw mode")
            msg.exec()
            return

        msg = QMessageBox()
        msg.setWindowTitle("Calibration")
        msg.setText("Place the board")
        msg.exec()

        # SEND CAMERA CALIBRATION REQUEST

        request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.ACTION_CALIBRATE,
                          Constants.REQUEST_RESOURCE_CAMERA)
        response = self.requestSender.sendRequest(request)
        print("Camera calib responce, ",response)
        response = Response.from_dict(response)


        if response.status == Constants.RESPONSE_STATUS_ERROR:
            request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.CAMERA_ACTION_RAW_MODE_OFF,
                              Constants.REQUEST_RESOURCE_CAMERA)
            self.requestSender.sendRequest(request)
            # show message dialog
            msg = QMessageBox()
            msg.setWindowTitle("Camera Calibration Failed")
            msg.setText(response.message)
            msg.exec()
            return


        msg = QMessageBox()
        msg.setWindowTitle("Camera Calibration Success")
        msg.setText("Move the chessboard")
        msg.exec()

        # SEND ROBOT CALIBRATION REQUEST
        print("Robot calib start")
        request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.ACTION_CALIBRATE, Constants.REQUEST_RESOURCE_ROBOT)
        response = self.requestSender.sendRequest(request)
        response = Response.from_dict(response)

        if response.status == Constants.RESPONSE_STATUS_ERROR:
            request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.CAMERA_ACTION_RAW_MODE_OFF,
                              Constants.REQUEST_RESOURCE_CAMERA)
            self.requestSender.sendRequest(request)
            print("Error calibrating robot")
            msg = QMessageBox()
            msg.setWindowTitle("Robot Calibration Failed")
            msg.setText(f"Error calibrating robot: {response.message}")
            msg.exec()
            return False, response.message

        # self.current_content.pause_feed(response.data['image'])
        # self.robotControl = RobotControl(self)
        # self.mainLayout.insertWidget(1, self.robotControl)
        return True, response.message

    def __manualMove(self):
        pass

    def updateCameraFeed(self):
        request = Request(req_type=Constants.REQUEST_TYPE_GET,
                          action=Constants.CAMERA_ACTION_GET_LATEST_FRAME,
                          resource=Constants.REQUEST_RESOURCE_CAMERA)
        responseDict = self.requestSender.sendRequest(request)
        response = Response.from_dict(responseDict)
        if response.status != Constants.RESPONSE_STATUS_SUCCESS:
            print("Error getting latest frame")
            return
        frame = response.data['frame']
        return frame

    def saveRobotCalibrationPoint(self):
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE,
                          action=Constants.ROBOT_ACTION_SAVE_POINT,
                          resource=Constants.REQUEST_RESOURCE_ROBOT)
        responseDict = self.requestSender.sendRequest(request)
        response = Response.from_dict(responseDict)

        if response.status == Constants.RESPONSE_STATUS_ERROR:
            print("Failed to save point")
            return False,False

        pointsCount = response.data.get("pointsCount", 0)  # Default to 0 if key is missing

        if pointsCount == 10:
            print("All points saved")
            return True,True

    def sendJogRequest(self, message: str):
        # Example message -> "robot/control/manual/jog/jogXMinus/10"
        parts = message.replace(JOG_ROBOT_TOPIC, "").strip("/").split("/")
        if len(parts) < 2:
            raise ValueError("Invalid jog message format")

        direction = parts[0]  # e.g., "jogXMinus"
        step = int(parts[1])  # e.g., 10

        # Process the jog request
        print(f"Direction: {direction}, Step: {step}")

        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE,
                          action=direction,
                          resource=Constants.REQUEST_RESOURCE_ROBOT,
                          data={"step": step})

        self.requestSender.sendRequest(request)