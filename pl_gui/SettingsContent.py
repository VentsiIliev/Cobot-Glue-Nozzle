import os

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import QTabWidget, QWidget, QSizePolicy

from .CustomWidgets import *

from .CameraSettingsTabLayout import CameraSettingsTabLayout
from .ContourSettingsTabLayout import ContourSettingsTabLayout
from .RobotSettingsTabLayout import RobotSettingsTabLayout
#
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

BACKGROUND = os.path.join(RESOURCE_DIR, "pl_ui_icons", "Background_&_Logo.png")
CAMERA_SETTINGS_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "CAMERA_SETTINGS_BUTTON.png")
CONTOUR_SETTINGS_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "CONTOUR_SETTINGS_BUTTON_SQUARE.png")
ROBOT_SETTINGS_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "ROBOT_SETTINGS_BUTTON_SQUARE.png")


class BackgroundWidget(CustomTabWidget):
    def __init__(self):
        super().__init__()

        # Load the background image
        self.background = QPixmap(BACKGROUND)  # Update with your image path
        if self.background.isNull():
            print("Error: Background image not loaded correctly!")

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background.isNull():
            print("Drawing the background image")
            painter.drawPixmap(self.rect(), self.background)  # Scale image to widget size
        else:
            print("Background image not loaded")
        super().paintEvent(event)  # Call the base class paintEvent to ensure proper widget rendering


class SettingsContent(BackgroundWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(""" 
            background-color: white; 
            padding: 10px; 
            QTabBar::tab { 
                background: transparent; 
                border: none; 
            } 
        """)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.cameraSettingsTab = BackgroundTabPage()
        self.robotSettingsTab = BackgroundTabPage()
        self.contourSettingsTab = BackgroundTabPage()

        self.addTab(self.cameraSettingsTab, "")
        self.addTab(self.robotSettingsTab, "")
        self.addTab(self.contourSettingsTab, "")

        # Set icons for tabs (Initial)
        self.update_tab_icons()

        # Tab content layouts
        self.cameraSettingsTabLayout = CameraSettingsTabLayout(self.cameraSettingsTab)
        self.robotSettingsTabLayout = RobotSettingsTabLayout(self.robotSettingsTab)
        self.contourSettingsTabLayout = ContourSettingsTabLayout(self.contourSettingsTab)

        self.hide()  # Hide settings content initially

    def update_tab_icons(self):
        """Dynamically update tab icons based on window width"""
        tab_icon_size = int(self.width() * 0.05)  # 5% of new window width for tabs
        self.setTabIcon(0, QIcon(CAMERA_SETTINGS_ICON_PATH))
        self.setTabIcon(1, QIcon(ROBOT_SETTINGS_ICON_PATH))
        self.setTabIcon(2, QIcon(CONTOUR_SETTINGS_ICON_PATH))
        self.tabBar().setIconSize(QSize(tab_icon_size, tab_icon_size))

    def resizeEvent(self, event):
        """Resize the tab widget dynamically on window resize"""
        new_width = self.width()

        # Resize the tab widget to be responsive to the window size
        self.setMinimumWidth(int(new_width * 0.3))  # 30% of the window width
        self.update_tab_icons()

        super().resizeEvent(event)

    def updateCameraSettings(self, cameraSettings):
        self.cameraSettingsTabLayout.updateValues(cameraSettings)

    def updateRobotSettings(self, robotSettings):
        self.robotSettingsTabLayout.updateValues(robotSettings)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SettingsContent()
    window.show()
    sys.exit(app.exec())
