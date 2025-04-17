import os
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QApplication, QFrame, QSizePolicy
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
CREATE_WORKPIECE_PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "PRESSED_CREATE_WORKPIECE_BUTTON_SQUARE.png")
CALIRATION_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "CALIBRATION_BUTTON_SQUARE.png")
CALIRATION__PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "PRESSED_CALIBRATION_BUTTON_SQUARE.png")
ROBOT_SETTINGS_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "ROBOT_SETTINGS_BUTTON_SQUARE.png")
ROBOT_SETTINGS_PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "PRESSSED_ROBOT_SETTINGS_BUTTON_SQUARE.png")
HOME_ROBOT_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "HOME_MACHINE_BUTTON.png")
STATIC_IMAGE_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "BACKGROUND_&_Logo.png")


class MainContent(QFrame):
    def __init__(self, screenWidth=1280, controller=None, parent=None):
        super().__init__()
        self.screenWidth = screenWidth
        self.parent = parent
        self.controller = controller
        self.setStyleSheet("background:transparent;")
        self.setContentsMargins(0, 0, 0, 0)

        # Main Layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(1)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Sidebar
        self.side_menu = self.create_side_menu()
        self.main_layout.addWidget(self.side_menu)

        # Stacked widget for dynamic content
        self.stacked_widget = QStackedWidget()
        self.content_area = QWidget()
        self.content_layout = QHBoxLayout()
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        self.content_area.setLayout(self.content_layout)

        # Add content area to stacked widget
        self.stacked_widget.addWidget(self.content_area)
        self.main_layout.addWidget(self.stacked_widget)

        # Camera Feed setup
        self.cameraFeed = CameraFeed(updateCallback=self.controller.updateCameraFeed)
        self.cameraFeed.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.content_layout.addWidget(self.cameraFeed, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)


        self.createWorkpieceForm = None
        self.manualMoveContent = None

    def create_side_menu(self):
        """Creates and returns the side menu widget."""
        self.buttons = [
            ButtonConfig(RUN_BUTTON_ICON_PATH, RUN_BUTTON_PRESSED_ICON_PATH, "Home", self.onStartButton),
            ButtonConfig(STOP_BUTTON_ICON_PATH, STOP_BUTTON_PRESSED_ICON_PATH, "Settings", self.onStopButton),
            ButtonConfig(CREATE_WORKPIECE_BUTTON_ICON_PATH, CREATE_WORKPIECE_PRESSED_BUTTON_ICON_PATH, "createWorkpiece", self.onCreateWorkpiece),
            ButtonConfig(CALIRATION_BUTTON_ICON_PATH, CALIRATION__PRESSED_BUTTON_ICON_PATH, "calibrate", self.onCalibrate),
            ButtonConfig(ROBOT_SETTINGS_BUTTON_ICON_PATH, ROBOT_SETTINGS_PRESSED_BUTTON_ICON_PATH, "manualMove", self.onManualMoveButton),
            ButtonConfig(HOME_ROBOT_BUTTON_ICON_PATH, HOME_ROBOT_BUTTON_ICON_PATH, "home robot", self.onHomeRobot),
            ButtonConfig(RUN_BUTTON_ICON_PATH, RUN_BUTTON_PRESSED_ICON_PATH, "DFX", self.dfxUpload),
        ]

        side_menu = Sidebar(self.screenWidth, self.buttons)
        side_menu.setContentsMargins(0, 0, 0, 0)
        return side_menu

    # Button Handlers
    def onStartButton(self):
        self.controller.sendRequest("start")

    def onStopButton(self):
        self.controller.sendRequest("robot/control/stop")

    def onCalibrate(self):
        result, message = self.controller.sendRequest("calibrate")
        if result:
            self.onManualMoveButton()
            self.manualMoveContent.savePointButton.show()
            self.manualMoveContent.onSaveCallback = self.controller.saveRobotCalibrationPoint

    def onHomeRobot(self):
        self.controller.sendRequest("robot/control/home")

    def onManualMoveButton(self):
        if self.manualMoveContent is None:
            if self.createWorkpieceForm:
                self.createWorkpieceForm.close()
                self.createWorkpieceForm = None
            self.manualMoveContent = ManualControlWidget(self, self.manualMoveCallback, self.controller.sendJogRequest)
            self.content_layout.addWidget(self.manualMoveContent)
        else:
            self.manualMoveContent.close()
            self.manualMoveContent = None

    def onCreateWorkpiece(self):
        # self.parent.show_contour_editor()
        if self.createWorkpieceForm is None:
            if self.manualMoveContent:
                self.manualMoveContent.close()
                self.manualMoveContent = None

            result, data = self.controller.sendRequest("createworkpiece")
            if result:
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
        self.side_menu.uncheck_all_buttons()
        sprayPattern = self.cameraFeed.getClickedPoints()

        data[WorkpieceField.SPRAY_PATTERN.value] = sprayPattern
        self.createWorkpieceForm = None
        self.cameraFeed.resume_feed()
        self.controller.saveWorkpiece(data)

    def dfxUpload(self):
        from PyQt6.QtWidgets import QFileDialog

        # Open file dialog to select a DXF file
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select DXF File",
            "",
            "DXF Files (*.dxf);;All Files (*)"
        )

        if file_name:
            print(f"Selected DXF file: {file_name}")
            from drawing.dxf.DxfParser import DXFPathExtractor
            extractor = DXFPathExtractor(file_name)
            wp, spray,fill = extractor.get_opencv_contours()
            print("✅ Workpiece Points:", wp)
            print("✅ Spray Pattern Points:", spray)
            print("✅ Fill Pattern Points:", fill)

            sprayPatternsDict ={
                "Contour":spray,
                "Fill": fill
            }


            from API.shared.workpiece.Workpiece import WorkpieceField
            data = {
                WorkpieceField.WORKPIECE_ID.value: 100,
                WorkpieceField.NAME.value: "From DFX",
                WorkpieceField.DESCRIPTION.value: "From DFX",
                WorkpieceField.TOOL_ID.value: "0",
                WorkpieceField.GRIPPER_ID.value: "0",
                WorkpieceField.GLUE_TYPE.value: "Type A",
                WorkpieceField.PROGRAM.value: "Trace",
                WorkpieceField.MATERIAL.value: "N/A",
                WorkpieceField.OFFSET.value: 0,
                WorkpieceField.HEIGHT.value: 4,
                WorkpieceField.SPRAY_PATTERN.value: sprayPatternsDict,
                WorkpieceField.CONTOUR.value: wp,
                WorkpieceField.CONTOUR_AREA.value : 0
            }

            self.controller.saveWorkpieceFromDXF(data)

    def resizeEvent(self, event):
        """Resize content and side menu dynamically."""
        super().resizeEvent(event)
        new_width = self.width()

        # Adjust icon sizes of the sidebar buttons
        icon_size = int(new_width * 0.05)  # 5% of the new window width
        for button in self.side_menu.buttons:
            button.setIconSize(QSize(icon_size, icon_size))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainContent(1280, app)
    window.show()
    sys.exit(app.exec())
