import os

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt6.QtWidgets import QMessageBox

from API.Request import Request
from API.Response import Response
from API import Constants

SETTINGS_STYLESHEET = os.path.join("GUI_NEW", "settings.qss")

class CalibrationMenu(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedWidth(400)
        self.parent.load_stylesheet(self, SETTINGS_STYLESHEET)
        self.initUI()

    def initUI(self):
        print("Calibration Menu")
        # add 3 buttons System Calibration, Camera Calibration Robot Calibration
        layout = QVBoxLayout()
        system_calibration_btn = QPushButton("System Calibration")
        camera_calibration_btn = QPushButton("Camera Calibration")
        robot_calibration_btn = QPushButton("Robot Calibration")
        system_calibration_btn.clicked.connect(self.system_calibration)
        camera_calibration_btn.clicked.connect(self.camera_calibration)
        robot_calibration_btn.clicked.connect(self.robot_calibration)
        layout.addWidget(system_calibration_btn)
        layout.addWidget(camera_calibration_btn)
        layout.addWidget(robot_calibration_btn)
        self.setLayout(layout)
        print("Calibration Menu UI setup")

    def system_calibration(self):
        result, message = self.parent.calibrate_camera()

        msg = QMessageBox()
        if not result:
            msg.setWindowTitle("Error")
            msg.setText(message)
        else:
            msg.setWindowTitle("Calibration")
            msg.setText("Move the chessboard")
        msg.exec()

        self.parent.on_calibrate_robot()
        self.parent.closeCalibrationMenu()

    def camera_calibration(self):
        result, message = self.parent.calibrate_camera()
        msg = QMessageBox()
        if not result:
            msg.setWindowTitle("Error")
            msg.setText(message)
        else:
            msg.setWindowTitle("Success")
            msg.setText(message)
        msg.exec()

    def robot_calibration(self):
        result, message = self.parent.on_calibrate_robot()



