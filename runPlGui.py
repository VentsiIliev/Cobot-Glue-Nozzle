from API.shared.settings.conreateSettings.CameraSettings import CameraSettings
from API.shared.settings.conreateSettings.RobotSettings import RobotSettings
from pl_gui.PlGui import PlGui

GET_SETTINGS_TOPIC = "settings/get"
START_TOPIC = "start"
STOP_TOPIC = "stop"
CREATE_WORKPIECE_TOPIC = "createworkpiece"
CALIBRATE_TOPIC = "calibrate"
MANUAL_MOVE_TOPIC = "robot/control/manual"
SAVE_ROBOT_CALIBRATION_POINT = "robot/control/manual/save"
JOG_ROBOT_TOPIC = "robot/control/manual/jog/"
UPDATE_CAMERA_FEED = "cameraFeed/update"


class MockController():
    def init(self):
        pass

    def sendRequest(self, message):
        if message == GET_SETTINGS_TOPIC:
            return self.__getSettings()

        print("Sending Request: ", message)
        return True, {"image": "MockImage",
                      "height": 4}

    def updateCameraFeed(self):
        pass

    def saveWorkpiece(self, data):
        print("Saving WP: ", data)

    def sendJogRequest(self, request):
        print("Sending Jog Request: ", request)

    def saveRobotCalibrationPoint(self):
        print("Saving Robot Point")

    def __getSettings(self):
        cameraSettings = CameraSettings()
        robotSettings = RobotSettings()
        return cameraSettings, robotSettings


if __name__ == "__main__":
    mockController = MockController()
    gui = PlGui(controller=mockController)
    gui.start()
