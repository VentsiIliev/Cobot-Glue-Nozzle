from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QApplication

from ButtonConfig import ButtonConfig
from CameraFeed import CameraFeed
from Sidebar import Sidebar
from CreateWorkpieceForm import CreateWorkpieceForm
from ManualControlWidget import ManualControlWidget


class MainContent(QWidget):
    def __init__(self, screenWidth, parent):
        super().__init__()
        self.screenWidth = screenWidth
        self.parent = parent
        self.setContentsMargins(0, 0, 0, 0)

        # Main layout for the content
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Create and add the side menu to the main content
        self.side_menu = self.create_side_menu()
        self.side_menu.alignItemsLeft()
        self.side_menu.alignItemsCenter()
        # add thin border
        self.main_layout.addWidget(self.side_menu)
        # add border

        # Main content area (center section)
        self.stacked_widget = QStackedWidget()
        self.setContentsMargins(0, 0, 0, 0)
        self.content_area = QWidget()
        self.content_area.setContentsMargins(0, 0, 0, 0)

        self.content_layout = QHBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # Add the content area to the stacked widget
        self.stacked_widget.addWidget(self.content_area)

        # Add the stacked widget to the main layout
        self.main_layout.addWidget(self.stacked_widget, 1)

        self.cameraFeed = CameraFeed()
        self.cameraFeedLayout = QVBoxLayout()
        self.content_layout.addWidget(self.cameraFeed)
        self.createWorkpieceForm = None
        self.manualMoveContent = None

    def create_side_menu(self):
        """Create a side menu inside the main content area."""

        self.startButtoncConfig = ButtonConfig("resources/pl_ui_icons/RUN_BUTTON.png",
                                               "resources/pl_ui_icons/PRESSED_RUN_BUTTON.png",
                                               "Home",
                                               self.onStartButton)
        self.stopButtonConfig = ButtonConfig("resources/pl_ui_icons/STOP_BUTTON.png",
                                             "resources/pl_ui_icons/PRESSED_STOP_BUTTON.png",
                                             "Settings",
                                             self.onStopButton)

        self.createWorkpieceConfig = ButtonConfig("resources/pl_ui_icons/CREATE_WORKPIECE_BUTTON_SQUARE.png",
                                                  "resources/pl_ui_icons/PRESSED_CREATE_WORKPIECE_BUTTON_SQUARE.png",
                                                  "createWorkpiece",
                                                  self.onCreateWorkpiece)

        self.calibrationButtonConfig = ButtonConfig("resources/pl_ui_icons/CALIBRATION_BUTTON_SQUARE.png",
                                                    "resources/pl_ui_icons/PRESSED_CALIBRATION_BUTTON_SQUARE.png",
                                                    "calibrate",
                                                    self.onButton4Clicked)

        self.manualMoveButtonConfig = ButtonConfig("resources/pl_ui_icons/ROBOT_SETTINGS_BUTTON_SQUARE.png",
                                                   "resources/pl_ui_icons/PRESSSED_ROBOT_SETTINGS_BUTTON_SQUARE.png",
                                                   "manualMove",
                                                   self.onManualMoveButton)

        self.buttons = [self.startButtoncConfig, self.stopButtonConfig, self.createWorkpieceConfig,
                        self.calibrationButtonConfig, self.manualMoveButtonConfig]

        side_menu = Sidebar(self.screenWidth, self.buttons)
        side_menu.setStyleSheet("background-color: white; padding: 0px;")
        side_menu.setContentsMargins(0, 0, 0, 0)
        return side_menu

    def onStartButton(self):
        print("Start clicked")

    def onStopButton(self):
        print("Stoped clicked")

    def onButton4Clicked(self):
        print("Button 4 clicked")

    def onManualMoveButton(self):
        if self.manualMoveContent is None:

            if self.createWorkpieceForm is not None:
                self.createWorkpieceForm.close()
                self.createWorkpieceForm = None

            self.manualMoveContent = ManualControlWidget(self,self.manualMoveCallbacl)
            self.content_layout.addWidget(self.manualMoveContent)
        else:
            self.manualMoveContent.close()
            self.manualMoveContent = None

    def onCreateWorkpiece(self):
        if self.createWorkpieceForm is None:

            if self.manualMoveContent is not None:
                self.manualMoveContent.close()
                self.manualMoveContent = None

            self.createWorkpieceForm = CreateWorkpieceForm(self,self.onCreateWorkpieceSubmit)
            self.content_layout.addWidget(self.createWorkpieceForm)
        else:
            self.createWorkpieceForm.close()
            self.createWorkpieceForm = None

    def manualMoveCallbacl(self):
        self.manualMoveContent = None

    def onCreateWorkpieceSubmit(self):
        print("Unchecking buttons")
        self.side_menu.uncheck_all_buttons()
        self.createWorkpieceForm = None

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
    window = MainContent(800, app)
    window.show()
    sys.exit(app.exec())
