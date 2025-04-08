from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTabWidget, QWidget, QSizePolicy

from .CameraSettingsTabLayout import CameraSettingsTabLayout
from .ContourSettingsTabLayout import ContourSettingsTabLayout
from .RobotSettingsTabLayout import RobotSettingsTabLayout

class SettingsContent(QTabWidget):
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

        # Add tabs
        self.cameraSettingsTab = QWidget()
        self.robotSettingsTab = QWidget()
        self.contourSettingsTab = QWidget()

        self.addTab(self.cameraSettingsTab, "")
        self.addTab(self.robotSettingsTab, "")
        self.addTab(self.contourSettingsTab, "")

        # Set icons for tabs (Initial)
        self.update_tab_icons()

        # Tab content layouts
        self.cameraSettingsTabLayout = CameraSettingsTabLayout(self.cameraSettingsTab)
        self.robotSettingsTabLayout = RobotSettingsTabLayout(self.robotSettingsTab)
        self.cameraSettingsTabLayout = ContourSettingsTabLayout(self.contourSettingsTab)

        self.hide()  # Hide settings content initially

    def update_tab_icons(self):
        """Dynamically update tab icons based on window width"""
        tab_icon_size = int(self.width() * 0.05)  # 5% of new window width for tabs
        self.setTabIcon(0, QIcon("resources/pl_ui_icons/CAMERA_SETTINGS_BUTTON.png"))
        self.setTabIcon(1, QIcon("resources/pl_ui_icons/ROBOT_SETTINGS_BUTTON_SQUARE.png"))
        self.setTabIcon(2, QIcon("resources/pl_ui_icons/CONTOUR_SETTINGS_BUTTON_SQUARE.png"))
        self.tabBar().setIconSize(QSize(tab_icon_size, tab_icon_size))

    def resizeEvent(self, event):
        """Resize the tab widget dynamically on window resize"""
        new_width = self.width()

        # Resize the tab widget to be responsive to the window size
        self.setMinimumWidth(int(new_width * 0.3))  # 30% of the window width
        self.update_tab_icons()

        super().resizeEvent(event)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SettingsContent()
    window.show()
    sys.exit(app.exec())
