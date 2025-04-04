import os
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QFrame
from PyQt6.QtCore import Qt

from API.Request import Request
from API import Constants
from API.shared.settings.conreateSettings.CameraSettings import CameraSettings
from API.shared.settings.conreateSettings.RobotSettings import RobotSettings
from API.Response import Response
from API.shared.workpiece.Workpiece import WorkpieceField


from GUI_NEW.SideMenu import SideMenu
from GUI_NEW.SettingsMenu.SettingsMenu import SettingsMenu
from GUI_NEW.ContentViews.HomeContent import HomeContent
from GUI_NEW.CreateWorkpieceMenu import CreateWorkpieceMenu
from GUI_NEW.Enums import Widget
from GUI_NEW.LoginDialog import LoginDialog
from GUI_NEW.RobotControl import RobotControl
from GUI_NEW.CalibrationMenu import CalibrationMenu

from GlueDispensingApplication.tools.enums.ToolID import ToolID
from GlueDispensingApplication.tools.enums.GlueType import GlueType
from GlueDispensingApplication.tools.enums.Program import Program
from GlueDispensingApplication.tools.enums.Gripper import Gripper

from PyQt6.QtWidgets import QMessageBox

# TEMPORARY IMPORTS
from GlueDispensingApplication.tools.GlueNozzleService import GlueNozzleService

PLACEHOLDER_IMAGE_PATH = os.path.join("GUI_NEW.py", "resources", "placeholder-image-1280x720-1.jpg")
WINDOW_TITLE = "PL Project"

class MainWindow(QMainWindow):
    def __init__(self, requestSender):
        super().__init__()

        self.requestSender = requestSender
        self.setWindowTitle(WINDOW_TITLE)

        # Set fixed window size
        #self.setFixedSize(1550, 720)
        # Enable full-screen mode
        self.showFullScreen()

        self.setStyleSheet("background-color: #F8F8F2;")
        self.is_logged_in = False
        # Remove OS window buttons
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint)
        #bind o nad p keys
        self.keyPressEvent = self.on_key_press
        self.initUI()

    def initUI(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.mainLayout = QHBoxLayout()
        centralWidget.setLayout(self.mainLayout)

    def setContentArea(self):
        self.contentArea = QFrame()
        self.contentArea.setStyleSheet("background-color: #F8F8F2;")
        self.mainLayout.addWidget(self.contentArea, 1)

    def setPlaceholderImage(self):
        self.current_content.set_image(PLACEHOLDER_IMAGE_PATH)

    def setHomeContentView(self, homeContentView):
        self.current_content = homeContentView
        self.mainLayout.addWidget(self.current_content)

    def setSideMenu(self, sideMenu):
        self.sideMenu = sideMenu
        self.mainLayout.addWidget(self.sideMenu)

    def on_key_press(self, event):
        # temp code to test glue nozzle
        if event.key() == Qt.Key.Key_O:
            glueNozzleService = GlueNozzleService()
            data = [1, 16, 4, 20, 30, 24000, 0, 3000, 0]
            glueNozzleService.sendCommand(data)
        elif event.key() == Qt.Key.Key_P:
            glueNozzleService = GlueNozzleService()
            data = [0, 16, 4, 20, 30, 24000, 0, 3000, 0]
            glueNozzleService.sendCommand(data)
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_F1:
            self.showNormal()


    def on_home(self):
        # Check if the current content is already HomeContent, if so, don't add it again.
        if not isinstance(self.current_content, HomeContent):
            # If the current content is not HomeContent, remove the old content
            self.current_content.setParent(None)
            # Create a new HomeContent widget
            self.current_content = HomeContent(self)
            self.mainLayout.addWidget(self.current_content)
            self.current_content.set_image(PLACEHOLDER_IMAGE_PATH)  # Update image
        print("Home button clicked")

    def create_workpiece(self):
        # Check if create workpiece menu is already open
        if hasattr(self, 'createWorkpieceMenu') and self.createWorkpieceMenu.isVisible():
            self.close_create_workpiece()
            return

        # if settings is open, close it before opening create workpiece
        if hasattr(self, 'settingsMenu') and self.settingsMenu.isVisible():
            self.close_settings()

        request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.ACTION_CREATE_WORKPIECE)
        response = self.sendRequest(request)
        response = Response.from_dict(response)
        print("Create Workpiece response: ", response)

        if response.status == Constants.RESPONSE_STATUS_ERROR:
            print("Error creating workpiece")
            QMessageBox.critical(self, "Error", response.message)
            return

        responseData = response.data
        #request the latest image
        # request = Request(Constants.REQUEST_TYPE_GET, Constants.REQUEST_ACTION_GET_LATEST_FRAME, Constants.REQUEST_RESOURCE_CAMERA)
        # response = self.requestSender.sendRequest(request)

        if response == Constants.RESPONSE_STATUS_ERROR:
            QMessageBox.critical(self, "Error", "Error getting latest frame")
            return

        # response = Response.from_dict(response)
        latestFrame = responseData['image']
        self.current_content.pause_feed(latestFrame)

        """
        Structure of the config dictionary:

        Keys: The keys are WorkpieceField enum values (e.g., WorkpieceField.WORKPIECE_ID, WorkpieceField.NAME, etc.).
              These represent the fields you want to include in your form.

        Values: Each value is a tuple consisting of:

            - Widget Type: Specifies the type of widget to be used for the field,
              either a QLineEdit (for text input) or QComboBox (for dropdown selection).

            - Default Value: A string or list, representing the default value or items to be displayed in the widget
              (e.g., options for a dropdown or a default text for a line edit).

            - Validation Flags: A dictionary containing key-value pairs that define validation rules for the field:
                - required: If set to True, the field must not be empty.
                - is_numeric: If set to True, the field must only contain numeric values (either integers or floating-point numbers).
        """

        config = {
            WorkpieceField.WORKPIECE_ID: (Widget.LINE_EDIT, "", {"required": True, "is_numeric": True}),
            WorkpieceField.NAME: (Widget.LINE_EDIT, "", {"required": True, "is_numeric": False}),
            WorkpieceField.DESCRIPTION: (Widget.LINE_EDIT, "", {"required": True, "is_numeric": False}),
            WorkpieceField.TOOL_ID: (
                Widget.DROPDOWN, [ToolID.Tool1.value, ToolID.Tool2.value, ToolID.Tool3.value],
                {"required": True, "is_numeric": True}),
            WorkpieceField.GRIPPER_ID: (
                Widget.DROPDOWN, [Gripper.SINGLE.value, Gripper.DOUBLE.value],
                {"required": True, "is_numeric": False}),
            WorkpieceField.GLUE_TYPE: (
                Widget.DROPDOWN, [GlueType.TypeA.value, GlueType.TypeB.value, GlueType.TypeC.value],
                {"required": True, "is_numeric": True}),
            WorkpieceField.PROGRAM: (
            Widget.DROPDOWN, [Program.TRACE.value, Program.ZIGZAG.value], {"required": True, "is_numeric": True}),
            WorkpieceField.MATERIAL: (Widget.LINE_EDIT, "", {"required": True, "is_numeric": False}),
            WorkpieceField.OFFSET: (Widget.LINE_EDIT, "", {"required": True, "is_numeric": True}),
            WorkpieceField.HEIGHT: (
                Widget.LINE_EDIT, str(responseData[WorkpieceField.HEIGHT.value]),
                {"required": True, "is_numeric": True}),
        }

        self.createWorkpieceMenu = CreateWorkpieceMenu(self, config)
        self.mainLayout.insertWidget(1, self.createWorkpieceMenu)
        self.sideMenu.create_workpieceBtn.setChecked(True)

    def sendWorkpieceData(self,wpData):
        clickedPoints = self.current_content.transformedPoints
        wpData[WorkpieceField.SPRAY_PATTERN.value] = clickedPoints
        request = Request(Constants.REQUEST_TYPE_POST, Constants.ACTION_SAVE_WORKPIECE,
                          Constants.REQUEST_RESOURCE_WORKPIECE, data=wpData)
        response = self.sendRequest(request)
        response = Response.from_dict(response)
        if response.status == Constants.RESPONSE_STATUS_ERROR:
            message = "Error saving workpiece"
            QMessageBox.critical(self, "Error", message)
            return False, response.message

        QMessageBox.information(self, "Success", "Workpiece saved successfully")
        return True, response.message


    def close_create_workpiece(self):
        self.createWorkpieceMenu.setParent(None)
        self.sideMenu.create_workpieceBtn.setChecked(False)
        self.current_content.resume_feed()

    def on_start(self):
        print("Start button clicked")
        response = self._sendExecuteRequest(Constants.ACTION_START)
        print("Start response: ", response)

        response = Response.from_dict(response)
        if response.status == Constants.RESPONSE_STATUS_ERROR:
            #check if the message is empty dict
            if not response.message:
                response.message = ""

            QMessageBox.critical(self, "Error", response.message)
            # return False, response.message
        self.sideMenu.startBtn.setChecked(False)

    def closeCalibrationMenu(self):
        self.calibrationMenu.setParent(None)
        self.sideMenu.calibrateBtn.setChecked(False)
        request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.CAMERA_ACTION_RAW_MODE_OFF,
                          Constants.REQUEST_RESOURCE_CAMERA)
        self.sendRequest(request)

    def calibrate_camera(self):
        request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.ACTION_CALIBRATE,
                          Constants.REQUEST_RESOURCE_CAMERA)
        response = self.sendRequest(request)
        response = Response.from_dict(response)
        print("Calibrate response: ", response)
        if response.status == Constants.RESPONSE_STATUS_ERROR:
            print("Error calibrating camera")
            return False, response.message

        return True,response.message


    def on_calibrate(self):
        print("Calibrate button clicked")
        # Check if calibration menu is already open
        if hasattr(self, 'calibrationMenu') and self.calibrationMenu.isVisible():
            self.closeCalibrationMenu()
            return

        # open calibration menu
        request= Request(Constants.REQUEST_TYPE_EXECUTE, Constants.CAMERA_ACTION_RAW_MODE_ON, Constants.REQUEST_RESOURCE_CAMERA)
        response = self.sendRequest(request)
        response = Response.from_dict(response)
        if response.status == Constants.RESPONSE_STATUS_ERROR:
            # show message dialog
            msg = QMessageBox()
            msg.setWindowTitle("Calibration")
            msg.setText("Error entering raw mode")
            msg.exec()
            return

        self.calibrationMenu = CalibrationMenu(self)
        self.mainLayout.insertWidget(1, self.calibrationMenu)


    def on_robot_control(self):
        # prevent opening multiple robot control windows
        if hasattr(self, 'robotControl') and self.robotControl.isVisible():
            print("Robot control already open")
            self.close_robot_control()
            return
        self.robotControl = RobotControl(self)
        self.mainLayout.insertWidget(1, self.robotControl)

    def on_calibrate_robot(self):
        print("Calibrate Robot button clicked")

        # prevent opening multiple robot control windows
        if hasattr(self, 'robotControl') and self.robotControl.isVisible():
            print("Robot control already open")
            self.close_robot_control()
            return

        request= Request(Constants.REQUEST_TYPE_EXECUTE, Constants.ACTION_CALIBRATE, Constants.REQUEST_RESOURCE_ROBOT)
        response = self.sendRequest(request)
        response = Response.from_dict(response)
        if response.status == Constants.RESPONSE_STATUS_ERROR:
            print("Error calibrating robot")
            return False, response.message
        self.current_content.pause_feed(response.data['image'])
        self.robotControl = RobotControl(self)
        self.mainLayout.insertWidget(1, self.robotControl)
        return True, response.message

    def close_robot_control(self):
        self.robotControl.setParent(None)
        self.current_content.resume_feed()

    def toggle_auth(self):
        self.is_logged_in = not self.is_logged_in
        self.sideMenu.loginBtn.setText("Logout" if self.is_logged_in else "Login")
        if not self.is_logged_in:  # If user is logging out
            print("User Logged Out")
            self.setEnabled(False)  # Disable the main window

            while True:  # Keep showing the login dialog until login is successful
                login = LoginDialog(parent=self)
                login.setParent(self, login.windowFlags())

                if login.exec():  # Login successful
                    print("Logged in successfully")
                    self.setEnabled(True)  # Enable the main window
                    self.is_logged_in = True
                    self.sideMenu.loginBtn.setText("Logout")  # Update button text
                    break  # Exit the loop on success
                else:
                    print("Login failed, showing login dialog again.")
        self.sideMenu.startBtn.setChecked(False)

    def on_settings(self):
        print("Settings button clicked")
        # Check if settings menu is already open
        if hasattr(self, 'settingsMenu') and self.settingsMenu.isVisible():
            print("Settings menu already open")
            self.close_settings()
            return

        # if workpiece menu is open, close it before opening settings
        if hasattr(self, 'createWorkpieceMenu') and self.createWorkpieceMenu.isVisible():
            print("CreateWorkpieceMenu menu already open")
            self.close_create_workpiece()
        # GET THE CAMERA SETTINGS
        request = Request(Constants.REQUEST_TYPE_GET, Constants.ACTION_GET_SETTINGS,
                          Constants.REQUEST_RESOURCE_CAMERA)
        response = self.sendRequest(request)
        response = Response.from_dict(response)
        settingsDict = response.data if response.status == Constants.RESPONSE_STATUS_SUCCESS else {}
        cameraSettings = CameraSettings(data=settingsDict)
        print("Camera settings received: ", response)

        # GET THE ROBOT SETTINGS
        request = Request(Constants.REQUEST_TYPE_GET, Constants.ACTION_GET_SETTINGS,
                          Constants.REQUEST_RESOURCE_ROBOT)
        response = self.sendRequest(request)
        response = Response.from_dict(response)
        settingsDict = response.data if response.status == Constants.RESPONSE_STATUS_SUCCESS else {}
        robotSettings = RobotSettings(data=settingsDict)

        self.settingsMenu = SettingsMenu(self, cameraSettings,robotSettings)
        self.mainLayout.insertWidget(1, self.settingsMenu)
        self.sideMenu.settingsBtn.setChecked(True)

    def close_settings(self):
        self.settingsMenu.setParent(None)
        self.sideMenu.settingsBtn.setChecked(False)

    def load_stylesheet(self, widget, stylesheet_path):
        try:
            with open(stylesheet_path, "r") as style_file:
                widget.setStyleSheet(style_file.read())
        except FileNotFoundError:
            print(f"Error: Stylesheet file '{stylesheet_path}' not found in {stylesheet_path}")

    def _sendExecuteRequest(self, command):
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE, action=command)
        print("Sending Request: ", request)
        return self.requestSender.sendRequest(request)

    def sendRequest(self, request):
        if request.action != Constants.CAMERA_ACTION_GET_LATEST_FRAME:
            print("Request sent: ", request)
        return self.requestSender.sendRequest(request)
