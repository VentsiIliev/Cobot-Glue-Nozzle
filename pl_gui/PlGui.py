import sys
from PyQt6.QtWidgets import QApplication

from GlueDispensingApplication.DomesticRequestSender import DomesticRequestSender
from GlueDispensingApplication.RequestHandler import RequestHandler

from pl_gui.MainWindow import MainWindow
from pl_gui.DashboardContent import MainContent
#
from .LoginWindow import LoginWindow
import os
DEFAULT_SCREEN_WIDTH = 1280
DEFAULT_SCREEN_HEIGHT = 720
WINDOW_TITLE = "PL Project"
SETTINGS_STYLESHEET = os.path.join("pl_gui","styles.qss")
class PlGui:

    def __init__(self, controller=None):
        self.controller = controller
        self.requires_login = False

    def start(self):
        app = QApplication(sys.argv)
        # Load stylesheet from file
        try:
            with open(SETTINGS_STYLESHEET, "r") as file:
                app.setStyleSheet(file.read())
                print("Stylesheets applied")
        except FileNotFoundError:
            print("Stylesheet file not found. Using default styles.")


        dashboardContent = MainContent(screenWidth=DEFAULT_SCREEN_WIDTH,controller=self.controller)

        window = MainWindow(dashboardContent,self.controller)
        dashboardContent.parent = window

        window.setWindowTitle(WINDOW_TITLE)
        window.setMinimumSize(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        window.setGeometry(100, 100, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        window.setContentsMargins(0, 0, 0, 0)

        dashboardContent.screenWidth = window.screen_width
        window.main_content = dashboardContent
        window.show()
        if self.requires_login:
            window.setEnabled(False)
            login = LoginWindow()
            if login.exec():  # This now blocks until login accepted/rejected
                print("Logged in successfully")
                window.setEnabled(True)
            else:
                print("Login failed or cancelled")
                return  # Instead of sys.exit(0), we just return and do not proceed

        sys.exit(app.exec())  # Only call this once after everything is set up


# if __name__ == "__main__":
#     gui = PlGui()
#     gui.start()