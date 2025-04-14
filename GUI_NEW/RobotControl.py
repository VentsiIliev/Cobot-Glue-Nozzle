from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
import os
from API.Request import Request
from API.Response import Response
from API import Constants

SETTINGS_STYLESHEET = os.path.join("GUI_NEW", "settings.qss")

class RobotControl(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedWidth(400)
        self.parent.load_stylesheet(self, SETTINGS_STYLESHEET)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Jog Step Input
        step_layout = QHBoxLayout()
        step_label = QLabel("Jog Step:")
        self.step_input = QLineEdit()
        self.step_input.setPlaceholderText("Enter jog step")
        step_layout.addWidget(step_label)
        step_layout.addWidget(self.step_input)
        layout.addLayout(step_layout)

        # X Axis Controls
        x_layout = QHBoxLayout()
        x_minus_btn = QPushButton("X-")
        x_plus_btn = QPushButton("X+")
        x_minus_btn.clicked.connect(self.jog_x_minus)
        x_plus_btn.clicked.connect(self.jog_x_plus)
        x_layout.addWidget(x_minus_btn)
        x_layout.addWidget(x_plus_btn)
        layout.addLayout(x_layout)

        # Y Axis Controls
        y_layout = QHBoxLayout()
        y_minus_btn = QPushButton("Y-")
        y_plus_btn = QPushButton("Y+")
        y_minus_btn.clicked.connect(self.jog_y_minus)
        y_plus_btn.clicked.connect(self.jog_y_plus)
        y_layout.addWidget(y_minus_btn)
        y_layout.addWidget(y_plus_btn)
        layout.addLayout(y_layout)

        # Z Axis Controls
        z_layout = QHBoxLayout()
        z_minus_btn = QPushButton("Z-")
        z_plus_btn = QPushButton("Z+")
        z_minus_btn.clicked.connect(self.jog_z_minus)
        z_plus_btn.clicked.connect(self.jog_z_plus)
        z_layout.addWidget(z_minus_btn)
        z_layout.addWidget(z_plus_btn)
        layout.addLayout(z_layout)

        # Save Point Button (make it an instance variable)
        self.savePoint_btn = QPushButton("Save Point")
        self.savePoint_btn.clicked.connect(self.on_save_point)
        layout.addWidget(self.savePoint_btn)

        self.setLayout(layout)

    def get_jog_step(self):
        try:
            return float(self.step_input.text())
        except ValueError:
            return 1.0  # Default jog step

    def jog_x_minus(self):
        step = self.get_jog_step()
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE,
                          action=Constants.ROBOT_ACTION_JOG_X_MINUS,
                          resource=Constants.REQUEST_RESOURCE_ROBOT,
                          data={"step": step})
        print(request.to_dict())
        self.parent.sendRequest(request)

    def jog_x_plus(self):
        step = self.get_jog_step()
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE,
                          action=Constants.ROBOT_ACTION_JOG_X_PLUS,
                          resource=Constants.REQUEST_RESOURCE_ROBOT,
                          data={"step": step})
        print(request.to_dict())
        self.parent.sendRequest(request)

    def jog_y_minus(self):
        step = self.get_jog_step()
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE,
                          action=Constants.ROBOT_ACTION_JOG_Y_MINUS,
                          resource=Constants.REQUEST_RESOURCE_ROBOT,
                          data={"step": step})
        print(request.to_dict())
        self.parent.sendRequest(request)

    def jog_y_plus(self):
        step = self.get_jog_step()
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE,
                          action=Constants.ROBOT_ACTION_JOG_Y_PLUS,
                          resource=Constants.REQUEST_RESOURCE_ROBOT,
                          data={"step": step})
        print(request.to_dict())
        self.parent.sendRequest(request)

    def jog_z_minus(self):
        step = self.get_jog_step()
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE,
                          action=Constants.ROBOT_ACTION_JOG_Z_MINUS,
                          resource=Constants.REQUEST_RESOURCE_ROBOT,
                          data={"step": step})
        print(request.to_dict())
        self.parent.sendRequest(request)

    def jog_z_plus(self):
        step = self.get_jog_step()
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE,
                          action=Constants.ROBOT_ACTION_JOG_Z_PLUS,
                          resource=Constants.REQUEST_RESOURCE_ROBOT,
                          data={"step": step})
        print(request.to_dict())
        self.parent.sendRequest(request)

    def on_save_point(self):
        request = Request(req_type=Constants.REQUEST_TYPE_EXECUTE,
                          action=Constants.ROBOT_ACTION_SAVE_POINT,
                          resource=Constants.REQUEST_RESOURCE_ROBOT)
        response = self.parent.sendRequest(request)
        response = Response.from_dict(response)

        if response.status == Constants.RESPONSE_STATUS_ERROR:
            print("Failed to save point")
            return

        pointsCount = response.data.get("pointsCount", 0)  # Default to 0 if key is missing

        if pointsCount == 10:
            print("All points saved")
            self.parent.close_robot_control()

