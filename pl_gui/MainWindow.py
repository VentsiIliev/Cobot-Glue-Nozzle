import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame
)
from pl_gui.SettingsContent import SettingsContent
from GlueDispensingApplication.tools.GlueNozzleService import GlueNozzleService
from .ButtonConfig import ButtonConfig
from .Header import Header
from .Sidebar import Sidebar
from pl_gui.GalleryContent import GalleryContent

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
DASHBOARD_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "DASHBOARD_BUTTON_SQUARE.png")
SETTINGS_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "SETTINGS_BUTTON.png")
SETTINGS_PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "PRESSED_SETTINGS_BUTTON.png")
GALLERY_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "LIBRARY_BUTTON_SQARE.png")
RUN_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "RUN_BUTTON.png")
RUN_PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "PRESSED_RUN_BUTTON.png")
LOGIN_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "LOGIN_BUTTON_SQUARE.png")
LOGIN_PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "PRESSED_RUN_BUTTON.png")
HELP_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "HELP_BUTTON_SQUARE.png")
HELP_PRESSED_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "PRESSED_HELP_BUTTON_SQUARE.png")


class MainWindow(QMainWindow):
    def __init__(self, dashboardWidget=None, controller=None):
        print("MainWindow init started")
        self.controller = controller
        super().__init__()

        self.keyPressEvent = self.on_key_press

        if dashboardWidget is None:
            print("Dash is none")
            self.main_content = QWidget()
        else:
            self.main_content = dashboardWidget
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #f0f0f0;")  # A light gray background instead of transparent
        # self.setStyleSheet("background-color: white;")  # A light gray background instead of transparent

        # Get screen size
        screen_size = QApplication.primaryScreen().size()

        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()

        # Main container widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout(self.central_widget)
        # Set spacing for the main layout
        self.main_layout.setSpacing(1)  # Set spacing to 10 pixels
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0 pixels
        self.content_layout = QHBoxLayout()  # Contains sidebar and main content

        # Header Section
        self.header = Header(self.screen_width, self.screen_height, self.toggle_menu)
        self.galleryContent = GalleryContent()
        # Sidebar Section
        dashboardButtonConfig = ButtonConfig(
            DASHBOARD_BUTTON_ICON_PATH,
            DASHBOARD_BUTTON_ICON_PATH,
            "",
            self.show_home
        )
        settingsButtonConfig = ButtonConfig(
            SETTINGS_BUTTON_ICON_PATH,
            SETTINGS_PRESSED_BUTTON_ICON_PATH,
            "",
            self.show_settings)

        galleryButtonConfig = ButtonConfig(
            GALLERY_BUTTON_ICON_PATH,
            GALLERY_BUTTON_ICON_PATH,
            "",
            self.onGalleryButton)

        helpButtonConfig = ButtonConfig(
            HELP_BUTTON_ICON_PATH,
            HELP_PRESSED_BUTTON_ICON_PATH,
            "",
            self.show_help)

        loginButtonConfig = ButtonConfig(
            LOGIN_BUTTON_ICON_PATH,
            LOGIN_PRESSED_BUTTON_ICON_PATH,
            "",
            self.show_login)
        self.sidebar = Sidebar(self.screen_width,
                               [dashboardButtonConfig, settingsButtonConfig, galleryButtonConfig],
                               [helpButtonConfig, loginButtonConfig])


        self.sidebar.setVisible(False)  # Make sidebar hidden by default

        self.sidebar.setStyleSheet("QWidget { background-color: white; }")

        # Create the QStackedWidget for content switching
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: white;")  # Set background color
        # Create content widgets and add them to the stacked widget
        # self.main_content = MainContent(self.screen_width)

        self.settings_content = SettingsContent()
        self.stacked_widget.addWidget(self.main_content)
        self.stacked_widget.addWidget(self.settings_content)
        self.stacked_widget.addWidget(self.galleryContent)

        # Add sidebar & stacked widget to content layout
        self.content_layout.addWidget(self.sidebar)

        self.content_layout.addWidget(self.stacked_widget, 1)  # Make stacked widget expand

        # Add header and content layout to main layout
        self.main_layout.addWidget(self.header)
        # add horizontal separator

        self.main_layout.addLayout(self.content_layout)

        print("MainWindow init finished")

    def on_key_press(self, event):
        # temp code to test glue nozzle
        if event.key() == Qt.Key.Key_O:
            glueNozzleService = GlueNozzleService()
            data = [1, 16, 4, 20, 80, 24000, 0, 1500, 0]
            glueNozzleService.sendCommand(data)
        elif event.key() == Qt.Key.Key_P:
            glueNozzleService = GlueNozzleService()
            data = [0, 16, 4, 20, 80, 24000, 0, 1500, 0]
            glueNozzleService.sendCommand(data)
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_F1:
            self.showNormal()

    def toggle_menu(self):
        """Show/Hide Sidebar and adjust layout"""
        is_visible = self.sidebar.isVisible()

        # Toggle sidebar visibility
        self.sidebar.setVisible(not is_visible)

        # Adjust the stretch factors based on sidebar visibility
        if is_visible:  # Sidebar was visible, now hide it
            self.content_layout.removeWidget(self.sidebar)
            self.content_layout.addWidget(self.stacked_widget, 1)  # Give more space to stacked widget
        else:  # Sidebar was hidden, now show it
            self.content_layout.insertWidget(0, self.sidebar)
            self.content_layout.addWidget(self.stacked_widget, 1)  # Adjust content area as needed

    def onGalleryButton(self):
        """Display Gallery Content"""
        print("Gallery Button Clicked")
        self.stacked_widget.setCurrentWidget(self.galleryContent)
        self.controller.sendRequest("Open Gallery")

    def show_home(self):
        """Show Main Content (Replace QWidget with MainContent)"""
        if isinstance(self.main_content, QWidget):  # Check if it’s the initial QWidget
            from .DashboardContent import MainContent  # Import only when needed
            self.main_content = MainContent(screenWidth=self.screen_width, controller=self.controller,
                                            parent=self)  # Replace with MainContent
            self.stacked_widget.addWidget(self.main_content)  # Add new widget to stacked widget
            self.stacked_widget.setCurrentWidget(self.main_content)  # Set it to current widget
        else:
            self.stacked_widget.setCurrentWidget(self.main_content)  # Already MainContent, just switch

        self.toggle_menu()

    def show_settings(self):
        """Show Settings Content with Tabs"""
        self.stacked_widget.setCurrentWidget(self.settings_content)
        cameraSettings, robotSettings = self.controller.sendRequest("settings/get")
        self.settings_content.updateCameraSettings(cameraSettings)
        self.settings_content.updateRobotSettings(robotSettings)
        print(cameraSettings)
        print(robotSettings)

    def show_help(self):
        """Display Help Content"""
        self.stacked_widget.setCurrentWidget(self.main_content)
        self.settings_content.setVisible(False)
        self.controller.sendRequest("show_help")

    def show_login(self):
        """Display Login Content"""
        print("Login Section: Enter your credentials.")
        self.controller.sendRequest("show_login")
        # self.main_content.main_label.setText("Login Section: Enter your credentials.")
        # self.stacked_widget.setCurrentWidget(self.main_content)
        # self.settings_content.setVisible(False)

    def resizeEvent(self, event):
        """Adjust icon sizes and layout on window resize"""
        new_width = self.width()
        icon_size = int(new_width * 0.05)  # 5% of new window width

        # Resize sidebar buttons by accessing them by index
        self.sidebar.buttons[0].setIconSize(QSize(icon_size, icon_size))  # Home button
        self.sidebar.buttons[1].setIconSize(QSize(icon_size, icon_size))  # Settings button
        self.sidebar.buttons[2].setIconSize(QSize(icon_size, icon_size))  # Help button
        self.sidebar.buttons[3].setIconSize(QSize(icon_size, icon_size))  # Login button
        self.sidebar.buttons[4].setIconSize(QSize(icon_size, icon_size))

        # Resize menu button's icon size
        self.header.menu_button.setIconSize(QSize(icon_size, icon_size))

        super().resizeEvent(event)

# Run the application
# app = QApplication(sys.argv)
