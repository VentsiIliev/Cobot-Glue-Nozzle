import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QApplication, QFrame

from .ButtonConfig import ButtonConfig
from .CameraFeed import CameraFeed
from .Sidebar import Sidebar
from .CreateWorkpieceForm import CreateWorkpieceForm
from .ManualControlWidget import ManualControlWidget
from .specific.enums.WorkpieceField import WorkpieceField

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
RUN_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "RUN_BUTTON.png")
RUN_BUTTON_PRESSED_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "PRESSED_RUN_BUTTON.png")
STOP_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "STOP_BUTTON.png")
STOP_BUTTON_PRESSED_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "PRESSED_STOP_BUTTON.png")
CREATE_WORKPIECE_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "CREATE_WORKPIECE_BUTTON_SQUARE.png")
CREATE_WORKPIECE_PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons",
                                                         "PRESSED_CREATE_WORKPIECE_BUTTON_SQUARE.png")
CALIRATION_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "CALIBRATION_BUTTON_SQUARE.png")
CALIRATION__PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons",
                                                    "PRESSED_CALIBRATION_BUTTON_SQUARE.png")
ROBOT_SETTINGS_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "ROBOT_SETTINGS_BUTTON_SQUARE.png")
ROBOT_SETTINGS_PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons",
                                                       "PRESSSED_ROBOT_SETTINGS_BUTTON_SQUARE.png")
HOME_ROBOT_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons",
                                           "HOME_MACHINE_BUTTON.png")
STATIC_IMAGE_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "BACKGROUND_&_Logo.png")


class MainContent(QFrame):
    def __init__(self, screenWidth=1280, controller=None, parent=None):
        print("MainContent init started")
        super().__init__()
        self.screenWidth = screenWidth
        self.parent = parent
        # self.setStyleSheet("background:blue;")
        self.setStyleSheet("background:transparent;")
        self.controller = controller
        self.setContentsMargins(0, 0, 0, 0)

        # Main layout for the content
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(1)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Create and add the side menu to the main content
        self.side_menu = self.create_side_menu()
        self.side_menu.alignItemsLeft()
        self.side_menu.alignItemsCenter()

        # add thin border
        self.main_layout.addWidget(self.side_menu)

        # Main content area (center section)
        self.stacked_widget = QStackedWidget()
        self.setContentsMargins(0, 0, 0, 0)
        self.content_area = QWidget()
        self.content_area.setContentsMargins(0, 0, 0, 0)

        self.content_layout = QHBoxLayout()
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(1)

        self.content_area.setLayout(self.content_layout)
        # Add the content area to the stacked widget
        self.stacked_widget.addWidget(self.content_area)

        # Add the stacked widget to the main layout
        self.main_layout.addWidget(self.stacked_widget, 1)

        self.cameraFeed = CameraFeed(updateCallback=self.controller.updateCameraFeed)
        self.cameraFeed.pause_feed(static_image=STATIC_IMAGE_PATH)
        self.cameraFeedLayout = QVBoxLayout()
        self.content_layout.addWidget(self.cameraFeed)
        self.createWorkpieceForm = None
        self.manualMoveContent = None
        print("MainContent init finished")

    def create_side_menu(self):
        """Create a side menu inside the main content area."""

        self.startButtoncConfig = ButtonConfig(RUN_BUTTON_ICON_PATH,
                                               RUN_BUTTON_PRESSED_ICON_PATH,
                                               "Home",
                                               self.onStartButton)
        self.stopButtonConfig = ButtonConfig(STOP_BUTTON_ICON_PATH,
                                             STOP_BUTTON_PRESSED_ICON_PATH,
                                             "Settings",
                                             self.onStopButton)

        self.createWorkpieceConfig = ButtonConfig(CREATE_WORKPIECE_BUTTON_ICON_PATH,
                                                  CREATE_WORKPIECE_PRESSED_BUTTON_ICON_PATH,
                                                  "createWorkpiece",
                                                  self.onCreateWorkpiece)

        self.calibrationButtonConfig = ButtonConfig(CALIRATION_BUTTON_ICON_PATH,
                                                    CALIRATION__PRESSED_BUTTON_ICON_PATH,
                                                    "calibrate",
                                                    self.onCalibrate)

        self.manualMoveButtonConfig = ButtonConfig(ROBOT_SETTINGS_BUTTON_ICON_PATH,
                                                   ROBOT_SETTINGS_PRESSED_BUTTON_ICON_PATH,
                                                   "manualMove",
                                                   self.onManualMoveButton)

        self.homeRobotButtonConfig = ButtonConfig(HOME_ROBOT_BUTTON_ICON_PATH,
                                                  HOME_ROBOT_BUTTON_ICON_PATH,
                                                  "home robot",
                                                  self.onHomeRobot)

        self.buttons = [self.startButtoncConfig, self.stopButtonConfig, self.createWorkpieceConfig,
                        self.calibrationButtonConfig, self.manualMoveButtonConfig, self.homeRobotButtonConfig]

        side_menu = Sidebar(self.screenWidth, self.buttons)
        # side_menu.setStyleSheet("background-color: white; padding: 0px;")
        side_menu.setContentsMargins(0, 0, 0, 0)
        # side_menu.setStyleSheet("QWidget { background-color: red; }")
        return side_menu

    def onStartButton(self):
        print("Start clicked")
        self.controller.sendRequest("start")

    def onStopButton(self):
        print("Stoped clicked")
        self.controller.sendRequest("robot/control/stop")

    def onCalibrate(self):
        print("Calibrate button clicked")
        result, message = self.controller.sendRequest("calibrate")

        if result:
            self.onManualMoveButton()
            self.manualMoveContent.savePointButton.show()
            self.manualMoveContent.onSaveCallback = self.controller.saveRobotCalibrationPoint

    def onHomeRobot(self):
        self.controller.sendRequest("robot/control/home")

    def onManualMoveButton(self):
        if self.manualMoveContent is None:

            if self.createWorkpieceForm is not None:
                self.createWorkpieceForm.close()
                self.createWorkpieceForm = None

            self.manualMoveContent = ManualControlWidget(self, self.manualMoveCallback, self.controller.sendJogRequest)
            self.content_layout.addWidget(self.manualMoveContent)
        else:
            self.manualMoveContent.close()
            self.manualMoveContent = None

    def onCreateWorkpiece(self):
        if self.createWorkpieceForm is None:

            if self.manualMoveContent is not None:
                self.manualMoveContent.close()
                self.manualMoveContent = None

            result, data = self.controller.sendRequest("createworkpiece")
            if not result:
                return
            frame = data['image']
            self.cameraFeed.pause_feed(static_image=frame)

            self.createWorkpieceForm = CreateWorkpieceForm(self.parent, self.onCreateWorkpieceSubmit)
            self.createWorkpieceForm.setHeigh(data[WorkpieceField.HEIGHT.value])
            self.content_layout.addWidget(self.createWorkpieceForm)
        else:
            self.createWorkpieceForm.close()
            self.createWorkpieceForm = None

    def manualMoveCallback(self):
        self.manualMoveContent = None

    def onCreateWorkpieceSubmit(self, data):
        print("Unchecking buttons")
        self.side_menu.uncheck_all_buttons()

        sprayPattern = []
        data[WorkpieceField.SPRAY_PATTERN.value] = sprayPattern
        self.createWorkpieceForm = None
        self.cameraFeed.resume_feed()
        self.controller.saveWorkpiece(data)

    def resizeEvent(self, event):
        """Resize content and side menu dynamically."""
        super().resizeEvent(event)
        new_width = self.width()

        # Adjust the side menu width if necessary
        side_menu_width = int(new_width * 0.2)  # 20% of the window width for the side menu
        # self.side_menu.setFixedWidth(side_menu_width)

        # Adjust the icon sizes of the sidebar buttons
        icon_size = int(new_width * 0.05)  # 5% of the new window width
        for button in self.side_menu.buttons:
            button.setIconSize(QSize(icon_size, icon_size))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainContent(1280, app)
    window.show()
    sys.exit(app.exec())
