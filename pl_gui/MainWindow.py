import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame
)
from pl_gui.SettingsContent import SettingsContent

from ButtonConfig import ButtonConfig
from Header import Header
from Sidebar import Sidebar
from pl_gui.GalleryContent import GalleryContent


class MainWindow(QMainWindow):
    def __init__(self,dashboardWidget=None):
        print("MainWindow init started")
        super().__init__()

        if dashboardWidget is None:
            print("Dash is none")
            self.main_content = QWidget()
        else:
            self.main_content = dashboardWidget


        # self.setStyleSheet("background-color: #f0f0f0;")  # A light gray background instead of transparent
        self.setStyleSheet("background-color: white;")  # A light gray background instead of transparent

        # Get screen size
        screen_size = QApplication.primaryScreen().size()

        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()

        # Main container widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout(self.central_widget)
        self.content_layout = QHBoxLayout()  # Contains sidebar and main content

        # Header Section
        self.header = Header(self.screen_width, self.screen_height, self.toggle_menu)
        self.galleryContent = GalleryContent()
        # Sidebar Section
        dashboardButtonConfig = ButtonConfig("resources/pl_ui_icons/DASHBOARD_BUTTON_SQUARE.png",
                                             "resources/pl_ui_icons/DASHBOARD_BUTTON_SQUARE.png",
                                             "Home",
                                             self.show_home)
        settingsButtonConfig = ButtonConfig("resources/pl_ui_icons/SETTINGS_BUTTON.png",
                                            "resources/pl_ui_icons/PRESSED_SETTINGS_BUTTON.png",
                                            "Settings",
                                            self.show_settings)

        galleryButtonConfig = ButtonConfig("resources/pl_ui_icons/LIBRARY_BUTTON_SQARE.png",
                                           "resources/pl_ui_icons/LIBRARY_BUTTON_SQARE.png",
                                           "Help",
                                           self.onGalleryButton)

        runButtonConfig = ButtonConfig("resources/pl_ui_icons/RUN_BUTTON.png",
                                       "resources/pl_ui_icons/PRESSED_RUN_BUTTON.png",
                                       "Help",
                                       self.show_help)

        loginButtonConfig = ButtonConfig("resources/pl_ui_icons/LOGIN_BUTTON_SQUARE.png",
                                         "resources/pl_ui_icons/PRESSED_RUN_BUTTON.png",
                                         "Login",
                                         self.show_login)
        self.sidebar = Sidebar(self.screen_width,
                               [dashboardButtonConfig, settingsButtonConfig, galleryButtonConfig],
                               [runButtonConfig, loginButtonConfig])
        self.sidebar.setVisible(False)  # Make sidebar hidden by default

        self.sidebar.setStyleSheet("QWidget { background-color: red; }")

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
        # Add a vertical separator
        separatorLabel = QFrame()
        separatorLabel.setFrameShape(QFrame.Shape.VLine)
        separatorLabel.setFrameShadow(QFrame.Shadow.Sunken)
        self.content_layout.addWidget(separatorLabel)
        self.content_layout.addWidget(self.stacked_widget, 1)  # Make stacked widget expand

        # Add header and content layout to main layout
        self.main_layout.addWidget(self.header)
        # add horizontal separator
        separatorLabel = QFrame()
        separatorLabel.setFrameShape(QFrame.Shape.HLine)
        separatorLabel.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(separatorLabel)
        self.main_layout.addLayout(self.content_layout)

        print("MainWindow init finished")

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

    def show_home(self):
        """Show Main Content (Replace QWidget with MainContent)"""
        if isinstance(self.main_content, QWidget):  # Check if it’s the initial QWidget
            from DashboardContent import MainContent  # Import only when needed
            self.main_content = MainContent(screenWidth=self.screen_width)  # Replace with MainContent
            self.stacked_widget.addWidget(self.main_content)  # Add new widget to stacked widget
            self.stacked_widget.setCurrentWidget(self.main_content)  # Set it to current widget
        else:
            self.stacked_widget.setCurrentWidget(self.main_content)  # Already MainContent, just switch

        self.toggle_menu()

    def show_settings(self):
        """Show Settings Content with Tabs"""
        self.stacked_widget.setCurrentWidget(self.settings_content)

    def show_help(self):
        """Display Help Content"""
        self.main_content.main_label.setText("Help Section: How can we assist you?")
        self.stacked_widget.setCurrentWidget(self.main_content)
        self.settings_content.setVisible(False)

    def show_login(self):
        """Display Login Content"""
        print("Login Section: Enter your credentials.")
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




