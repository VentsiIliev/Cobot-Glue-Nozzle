import sys
from PyQt6.QtWidgets import QApplication

from pl_gui.MainWindow import MainWindow
from pl_gui.DashboardContent import MainContent
#
from LoginWindow import LoginWindow

class PlGUi:
    def __init__(self, controller=None):  # <-- FIXED here
        self.controller = controller
        self.requires_login = True

    def start(self):
        print("In start")
        app = QApplication(sys.argv)
        # Load stylesheet from file
        try:
            with open("styles.qss", "r") as file:
                app.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Stylesheet file not found. Using default styles.")


        dashboardContent = MainContent(screenWidth=1280)

        window = MainWindow( dashboardContent)

        window.setWindowTitle("PL Project")
        window.setMinimumSize(1280, 720)
        window.setGeometry(100, 100, 1280, 720)
        window.setContentsMargins(0, 0, 0, 0)

        dashboardContent.screenWidth = window.screen_width
        window.main_content = dashboardContent
        print("before window.show")
        window.show()
        print("Login needed: ", self.requires_login)
        if self.requires_login:
            print("Login needed")
            window.setEnabled(False)
            login = LoginWindow()
            if login.exec():  # This now blocks until login accepted/rejected
                print("Logged in successfully")
                window.setEnabled(True)
            else:
                print("Login failed or cancelled")
                return  # Instead of sys.exit(0), we just return and do not proceed

        sys.exit(app.exec())  # Only call this once after everything is set up


if __name__ == "__main__":
    gui = PlGUi()
    gui.start()