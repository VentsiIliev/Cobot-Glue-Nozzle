import tkinter as tk
from tkinter import ttk

from API.Request import Request
from API.Response import Response
from API import Constants
from API.shared.settings.conreateSettings.CameraSettings import CameraSettings
from API.shared.settings.conreateSettings.RobotSettings import RobotSettings
from API.shared.settings.conreateSettings.enums.CameraSettingKey import CameraSettingKey
from API.shared.settings.conreateSettings.enums.RobotSettingKey import RobotSettingKey
from API.RequestSender import RequestSender
class SettingsDialog:
    SAVE_BTN_TEXT = "Save"
    def __init__(self, parent, requestSender:RequestSender, responseHandler):
        # self.actionManager = actionManager
        self.requestSender = requestSender
        self.responseHandler = responseHandler
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Service")
        self.dialog.geometry("300x500")  # Increased window size

        notebook = ttk.Notebook(self.dialog)
        notebook.pack(expand=True, fill="both")

        self.nozzle_frame = ttk.Frame(notebook)
        self.camera_system_frame = ttk.Frame(notebook)
        self.robot_frame = ttk.Frame(notebook)

        notebook.add(self.nozzle_frame, text="Nozzle")
        notebook.add(self.camera_system_frame, text="Camera System")
        notebook.add(self.robot_frame, text="Robot")

        self.camera_notebook = ttk.Notebook(self.camera_system_frame)
        self.camera_notebook.pack(expand=True, fill="both")

        self.camera_frame = ttk.Frame(self.camera_notebook)
        self.camera_notebook.add(self.camera_frame, text="Camera")

        # self.brightness_frame = ttk.Frame(self.camera_notebook)
        # self.camera_notebook.add(self.brightness_frame, text="Brightness Controller")

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)  # Bind event to tab change

        self.create_nozzle_tab()
        self.create_camera_system_tab()
        # self.create_brightness_controller_tab()
        self.create_robot_tab()

        self.current_tab = self.nozzle_frame  # Default to tools tab

    def on_tab_changed(self, event):
        notebook = event.widget
        selected_tab = notebook.select()  # Get the currently selected tab
        self.current_tab = notebook.nametowidget(selected_tab)  # Update the current tab
        # print(f"Current tab: {self.current_tab}")  # For debugging

    def create_nozzle_tab(self):
        self.radioMode = tk.StringVar(value="Mode1")
        ttk.Label(self.nozzle_frame, text="Mode:").grid(row=0, column=0, padx=5, pady=5)
        modes = ["Mode1", "Mode2", "Mode3"]
        for i, mode in enumerate(modes):
            ttk.Radiobutton(self.nozzle_frame, text=mode, variable=self.radioMode, value=mode).grid(row=0, column=i + 1,
                                                                                                    padx=5, pady=5)

        self.buttonCommand = tk.StringVar()
        ttk.Label(self.nozzle_frame, text="Command:").grid(row=1, column=0, padx=5, pady=5)
        commandOptions = ["Start", "Stop", "Reset"]
        commandMenu = ttk.Combobox(self.nozzle_frame, textvariable=self.buttonCommand, values=commandOptions,
                                   state="readonly")
        commandMenu.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        commandMenu.current(0)

        fields = ["DropNr", "DropDist", "Frequency", "Volt Pos", "Volt Neg", "Time Pos", "Time Neg"]
        self.entryVars = [tk.StringVar() for _ in fields]

        for i, field in enumerate(fields):
            ttk.Label(self.nozzle_frame, text=f"{field}:").grid(row=i + 2, column=0, padx=5, pady=5)
            ttk.Entry(self.nozzle_frame, textvariable=self.entryVars[i]).grid(row=i + 2, column=1, columnspan=2, padx=5,
                                                                              pady=5)

        ttk.Button(self.nozzle_frame, text="Submit", command=self.submit).grid(row=len(fields) + 2, column=0,
                                                                               columnspan=3, pady=10)

    def create_camera_system_tab(self):
        request = Request(Constants.REQUEST_TYPE_GET, Constants.ACTION_GET_SETTINGS,
                          Constants.REQUEST_RESOURCE_CAMERA)

        response = self.requestSender.sendRequest(request)
        response = Response.from_dict(response)

        settingsDict = response.data if response.status == Constants.RESPONSE_STATUS_SUCCESS else {}
        if response.status != Constants.RESPONSE_STATUS_SUCCESS:
            self.responseHandler.handleResponse(response)

        self.cameraSettings = CameraSettings(data=settingsDict)

        ttk.Label(self.camera_frame, text=CameraSettingKey.INDEX.value).pack()
        self.index_entry = ttk.Entry(self.camera_frame)
        self.index_entry.pack()
        self.index_entry.insert(0, self.cameraSettings.get_camera_index())

        ttk.Label(self.camera_frame, text=CameraSettingKey.WIDTH.value).pack()
        self.width_entry = ttk.Entry(self.camera_frame)
        self.width_entry.pack()
        self.width_entry.insert(0, self.cameraSettings.get_camera_width())

        ttk.Label(self.camera_frame, text=CameraSettingKey.HEIGHT.value).pack()
        self.height_entry = ttk.Entry(self.camera_frame)
        self.height_entry.pack()
        self.height_entry.insert(0, self.cameraSettings.get_camera_height())

        ttk.Label(self.camera_frame, text=CameraSettingKey.SKIP_FRAMES.value).pack()
        self.skip_frames_entry = ttk.Entry(self.camera_frame)
        self.skip_frames_entry.pack()
        self.skip_frames_entry.insert(0, self.cameraSettings.get_skip_frames())

        ttk.Label(self.camera_frame, text=CameraSettingKey.THRESHOLD.value).pack()
        self.threshold_entry = ttk.Entry(self.camera_frame)
        self.threshold_entry.pack()
        self.threshold_entry.insert(0, self.cameraSettings.get_threshold())

        ttk.Label(self.camera_frame, text=CameraSettingKey.EPSILON.value).pack()
        self.epsilon_entry = ttk.Entry(self.camera_frame)
        self.epsilon_entry.pack()
        self.epsilon_entry.insert(0, self.cameraSettings.get_epsilon())

        ttk.Label(self.camera_frame, text=CameraSettingKey.CONTOUR_DETECTION.value).pack()
        self.contour_detection_var = tk.BooleanVar()
        self.contour_detection_var.set(self.cameraSettings.get_contour_detection())
        ttk.Checkbutton(self.camera_frame, variable=self.contour_detection_var).pack()

        ttk.Label(self.camera_frame, text=CameraSettingKey.DRAW_CONTOURS.value).pack()
        self.draw_contours_var = tk.BooleanVar()
        self.draw_contours_var.set(self.cameraSettings.get_draw_contours())
        ttk.Checkbutton(self.camera_frame, variable=self.draw_contours_var).pack()

        ttk.Button(self.camera_frame, text=self.SAVE_BTN_TEXT, command=self.save_camera_settings).pack()

    def create_brightness_controller_tab(self):
        ttk.Label(self.brightness_frame, text="Kp").pack()
        self.kp_entry = ttk.Entry(self.brightness_frame)
        self.kp_entry.pack()

        ttk.Label(self.brightness_frame, text="Ki").pack()
        self.ki_entry = ttk.Entry(self.brightness_frame)
        self.ki_entry.pack()

        ttk.Label(self.brightness_frame, text="Kd").pack()
        self.kd_entry = ttk.Entry(self.brightness_frame)
        self.kd_entry.pack()

        ttk.Label(self.brightness_frame, text="Set Point").pack()
        self.set_point_entry = ttk.Entry(self.brightness_frame)
        self.set_point_entry.pack()

        ttk.Button(self.brightness_frame, text=self.SAVE_BTN_TEXT, command=self.save_brightness_settings).pack()

    def create_robot_tab(self):
        request = Request(Constants.REQUEST_TYPE_GET, Constants.ACTION_GET_SETTINGS, Constants.REQUEST_RESOURCE_ROBOT)

        response = self.requestSender.sendRequest(request)
        response = Response.from_dict(response)

        if response.status == Constants.RESPONSE_STATUS_SUCCESS:
            settingsDict = response.data
            print(f"Response: {response}")
        else:
            settingsDict = {}
            self.responseHandler.handleResponse(response)

        self.robotSettings = RobotSettings(data=settingsDict)  # Store robot settings in self.robotSettings

        ttk.Label(self.robot_frame, text=RobotSettingKey.IP_ADDRESS.value).pack()
        self.ip_entry = ttk.Entry(self.robot_frame)
        self.ip_entry.pack()
        self.ip_entry.insert(0, self.robotSettings.get_robot_ip())

        ttk.Label(self.robot_frame, text=RobotSettingKey.VELOCITY.value).pack()
        self.velocity_entry = ttk.Entry(self.robot_frame)
        self.velocity_entry.pack()
        self.velocity_entry.insert(0, self.robotSettings.get_robot_velocity())

        ttk.Label(self.robot_frame, text=RobotSettingKey.ACCELERATION.value).pack()
        self.acceleration_entry = ttk.Entry(self.robot_frame)
        self.acceleration_entry.pack()
        self.acceleration_entry.insert(0, self.robotSettings.get_robot_acceleration())

        ttk.Label(self.robot_frame, text=RobotSettingKey.TOOL.value).pack()
        self.tool_entry = ttk.Entry(self.robot_frame)
        self.tool_entry.pack()
        self.tool_entry.insert(0, self.robotSettings.get_robot_tool())

        ttk.Label(self.robot_frame, text=RobotSettingKey.USER.value).pack()
        self.user_entry = ttk.Entry(self.robot_frame)
        self.user_entry.pack()
        self.user_entry.insert(0, self.robotSettings.get_robot_user())

        ttk.Button(self.robot_frame, text=self.SAVE_BTN_TEXT, command=self.save_robot_settings).pack()

    def save_robot_settings(self):
        # Save robot settings from UI components
        self.robotSettings.set_robot_ip(self.ip_entry.get())
        self.robotSettings.set_robot_velocity(int(self.velocity_entry.get()))
        self.robotSettings.set_robot_acceleration(int(self.acceleration_entry.get()))
        self.robotSettings.set_robot_tool(int(self.tool_entry.get()))
        self.robotSettings.set_robot_user(int(self.user_entry.get()))

        # Create a dictionary with the settings
        settings = {
            "header": "Robot",
            RobotSettingKey.IP_ADDRESS.value: self.robotSettings.get_robot_ip(),
            RobotSettingKey.VELOCITY.value: self.robotSettings.get_robot_velocity(),
            RobotSettingKey.ACCELERATION.value: self.robotSettings.get_robot_acceleration(),
            RobotSettingKey.TOOL.value: self.robotSettings.get_robot_tool(),
            RobotSettingKey.USER.value: self.robotSettings.get_robot_user()
        }

        request = Request(Constants.REQUEST_TYPE_POST, Constants.ACTION_SET_SETTINGS, Constants.REQUEST_RESOURCE_ROBOT, settings)
        response = self.requestSender.sendRequest(request)
        response = Response.from_dict(response)
        print(f"Response: {response}")
        self.responseHandler.handleResponse(response)

    def save_camera_settings(self):
        # Save camera settings from UI components
        self.cameraSettings.set_camera_index(int(self.index_entry.get()))
        self.cameraSettings.set_width(int(self.width_entry.get()))
        self.cameraSettings.set_height(int(self.height_entry.get()))
        self.cameraSettings.set_skip_frames(int(self.skip_frames_entry.get()))
        self.cameraSettings.set_threshold(int(self.threshold_entry.get()))
        self.cameraSettings.set_epsilon(float(self.epsilon_entry.get()))
        self.cameraSettings.set_contour_detection(self.contour_detection_var.get())
        self.cameraSettings.set_draw_contours(self.draw_contours_var.get())
        # Create a dictionary with the settings
        settings = {
            "header": "Camera",
            CameraSettingKey.INDEX.value: self.cameraSettings.get_camera_index(),
            CameraSettingKey.WIDTH.value: self.cameraSettings.get_camera_width(),
            CameraSettingKey.HEIGHT.value: self.cameraSettings.get_camera_height(),
            CameraSettingKey.SKIP_FRAMES.value: self.cameraSettings.get_skip_frames(),
            CameraSettingKey.THRESHOLD.value: self.cameraSettings.get_threshold(),
            CameraSettingKey.EPSILON.value: self.cameraSettings.get_epsilon(),
            CameraSettingKey.CONTOUR_DETECTION.value: self.cameraSettings.get_contour_detection(),
            CameraSettingKey.DRAW_CONTOURS.value: self.cameraSettings.get_draw_contours()
        }

        request = Request(Constants.REQUEST_TYPE_POST, Constants.ACTION_SET_SETTINGS, Constants.REQUEST_RESOURCE_CAMERA, settings)
        response = self.requestSender.sendRequest(request)
        response = Response.from_dict(response)
        print(f"Response: {response}")
        self.responseHandler.handleResponse(response)

    def save_brightness_settings(self):
        # Save brightness controller settings from UI components
        kp = float(self.kp_entry.get())
        ki = float(self.ki_entry.get())
        kd = float(self.kd_entry.get())
        set_point = float(self.set_point_entry.get())

        # Create a dictionary with the settings
        settings = {
            "header": "BrightnessController",
            "Kp": kp,
            "Ki": ki,
            "Kd": kd,
            "setPoint": set_point
        }

        request = Request(Constants.REQUEST_TYPE_POST, Constants.ACTION_SET_SETTINGS, Constants.REQUEST_RESOURCE_CAMERA, settings)
        response  = self.requestSender.sendRequest(request)
        response = Response.from_dict(response)
        print(f"Response: {response}")
        self.responseHandler.handleResponse(response)

    def submit(self):
        values = {
            'mode': self.radioMode.get(),
            'command': self.buttonCommand.get(),
            'dropNr': self.entryVars[0].get(),
            'dropDist': self.entryVars[1].get(),
            'frequency': self.entryVars[2].get(),
            'voltPos': self.entryVars[3].get(),
            'voltNeg': self.entryVars[4].get(),
            'timePos': self.entryVars[5].get(),
            'timeNeg': self.entryVars[6].get(),
        }

        if values['command'] == "Stop":
            request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.ACTION_STOP, Constants.REQUEST_RESOURCE_GLUE_NOZZLE)
            response = self.requestSender.sendRequest(request)
            response = Response.from_dict(response)
            if response.status != Constants.RESPONSE_STATUS_SUCCESS:
                self.responseHandler.handleResponse(response)
            return

        command = 16 if values['command'] == "Start" else 0
        mode = {"Mode1": 1, "Mode2": 2, "Mode3": 3}.get(values['mode'], 1)

        data = [
            mode, command,
            int(values['dropNr']), int(values['dropDist']),
            int(values['frequency']), int(values['voltPos']),
            int(values['voltNeg']), int(values['timePos']), int(values['timeNeg'])
        ]

        request = Request(Constants.REQUEST_TYPE_EXECUTE, Constants.ACTION_START, Constants.REQUEST_RESOURCE_GLUE_NOZZLE, data)
        response = self.requestSender.sendRequest(request)
        print(f"Response: {response}")
        response = Response.from_dict(response)
        if response.status != Constants.RESPONSE_STATUS_SUCCESS:
            self.responseHandler.handleResponse(response)