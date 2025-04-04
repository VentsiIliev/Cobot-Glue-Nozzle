from GUI_NEW.MainWindowNew import MainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QLoggingCategory
from GUI_NEW.LoginDialog import LoginDialog
from GUI_NEW.SideMenu import SideMenu
from GUI_NEW.ContentViews.HomeContent import HomeContent
import sys
import os

class GUI_NEW():
    def __init__(self, requestSender):
        self.requestSender = requestSender
        self.requires_login = False

    def start(self):
        # Configure logging
        os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
        QLoggingCategory.setFilterRules("""
                               qt.pointer.velocity=false
                               qt.qpa.uiautomation=false
                           """)
        os.environ["QT_LOGGING_RULES"] = "qt.pointer.velocity=false"
        self.app = QApplication(sys.argv)

        # Create the main window but disable it initially
        self.window = MainWindow(self.requestSender)

        # Create and configure the side menu
        self.setupSideMenu()

        self.homeContent = HomeContent(self.window)

        self.window.setSideMenu(self.sideMenu)
        self.window.setContentArea()
        self.window.setHomeContentView(self.homeContent)

        self.window.show()

        if self. requires_login:
            # Create and show the login dialog
            self.window.setEnabled(False)
            self.login = LoginDialog(parent=self.window)
            self.login.setParent(self.window, self.login.windowFlags())
            if self.login.exec():  # Show login dialog and check if login succeeds
                print("Logged in successfully")
                self.window.setEnabled(True)  # Enable the main window
                self.window.toggle_auth()
                sys.exit(self.app.exec())  # Start the event loop
            else:
                print("Login failed")
        else:
            sys.exit(self.app.exec())

    def setupSideMenu(self):
        self.sideMenu = SideMenu(self.window, 250, "PL Project")
        sideMenuButtons = [
            # ("Home", self.parent.on_home, HOME_ICON_PATH), # COMMENTED OUT BECAUSE IT'S NOT USED
            ("Start", self.window.on_start, "path/to/start_icon.png"),
            ("Calibrate", self.window.on_calibrate, "path/to/calibrate_icon.png"),
            # ("Calibrate Robot", self.parent.on_calibrate_robot, "path/to/calibrate_icon.png"),
            ("Robot Control", self.window.on_robot_control, "path/to/calibrate_icon.png"),
            ("Settings", self.window.on_settings, "path/to/settings_icon.png"),
            ("Create Workpiece", self.window.create_workpiece, "path/to/create_icon.png"),
        ]
        self.sideMenu.setButtons(sideMenuButtons)
        self.sideMenu.addSpacer()
        loginButtonConfig = ["Login", self.window.toggle_auth, "path/to/login_icon.png"]
        self.sideMenu.setButtons([loginButtonConfig])
