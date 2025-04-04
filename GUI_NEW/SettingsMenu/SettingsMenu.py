# settings_menu.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTabWidget, QPushButton
from PyQt6.QtCore import Qt
from GUI_NEW.SettingsMenu.SettingsTab import SettingsTab
import os
from API.shared.settings.conreateSettings.enums.CameraSettingKey import CameraSettingKey
from API.shared.settings.conreateSettings.enums.RobotSettingKey import RobotSettingKey
from GUI_NEW.Enums import Widget
from API import Constants

SETTINGS_STYLESHEET = os.path.join("GUI_NEW", "settings.qss")

class SettingsMenu(QFrame):
    def __init__(self, main_window,cameraSettings,robotSettings): # TODO: PASS THE ACTUAL ROBOT SETTINGS
        super().__init__()
        self.main_window = main_window
        self.setFixedWidth(400)
        self.setStyleSheet("background-color: #495474; color: #F8F8F2;")
        self.main_window.load_stylesheet(self, SETTINGS_STYLESHEET)
        self.cameraSettings = cameraSettings
        self.robotSettings = robotSettings
        self.initUI()

    def initUI(self):
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.settingsLayout)

        settingsTitle = QLabel("Settings")
        self.settingsLayout.addWidget(settingsTitle)

        self.settingsTabs = QTabWidget()
        # self.settingsTabs.setStyleSheet("background-color: #6272a4; color: #F8F8F2; border: none;")
        self.settingsLayout.addWidget(self.settingsTabs)


        # TODO MAYBE CREATE A BASE SETTINGS TAB THAT TAKES A SETTINGS OBJECT AND CREATES THE TAB BASED ON THE SETTINGS
        cameraTabConfig = {
            "header": Constants.REQUEST_RESOURCE_CAMERA,
            CameraSettingKey.INDEX: (Widget.LINE_EDIT,{"is_numeric": True,"type": int}),
            CameraSettingKey.WIDTH: (Widget.LINE_EDIT,{"is_numeric": True,"type": int}),
            CameraSettingKey.HEIGHT: (Widget.LINE_EDIT,{"is_numeric": True,"type": int}),
            CameraSettingKey.SKIP_FRAMES: (Widget.LINE_EDIT,{"is_numeric": True,"type": int}),
            CameraSettingKey.THRESHOLD: (Widget.LINE_EDIT,{"is_numeric": True,"type": int}),
            CameraSettingKey.EPSILON: (Widget.LINE_EDIT,{"is_numeric": True,"type": float}),
            CameraSettingKey.CONTOUR_DETECTION: (Widget.CHECKBOX,{"is_numeric": False,"type": bool}),
            CameraSettingKey.DRAW_CONTOURS: (Widget.CHECKBOX,{"is_numeric": False,"type": bool})
        }

        robotTabConfig={
            "header": Constants.REQUEST_RESOURCE_ROBOT,
            RobotSettingKey.IP_ADDRESS: (Widget.LINE_EDIT,{"is_numeric": False,"type": str}),
            RobotSettingKey.VELOCITY: (Widget.LINE_EDIT,{"is_numeric": True,"type": int}),
            RobotSettingKey.ACCELERATION: (Widget.LINE_EDIT,{"is_numeric": True,"type": int}),
            RobotSettingKey.TOOL: (Widget.LINE_EDIT,{"is_numeric": False,"type": int}),
            RobotSettingKey.USER: (Widget.LINE_EDIT,{"is_numeric": False,"type": int})
        }

        self.settingsTabs.addTab(SettingsTab(self.main_window, [(self.cameraSettings, cameraTabConfig, CameraSettingKey)]), "Camera System")
        self.settingsTabs.addTab(SettingsTab(self.main_window, [(self.robotSettings, robotTabConfig, RobotSettingKey)]), "Robot")

        # Apply stylesheet to each tab
        for i in range(self.settingsTabs.count()):
            tab = self.settingsTabs.widget(i)
            self.main_window.load_stylesheet(tab, SETTINGS_STYLESHEET)

        backBtn = QPushButton("Back")# TODO THIS HARD CODED BACK BUTTON LABEL SHOULD BE REMOVED
        backBtn.clicked.connect(self.main_window.close_settings)
        self.settingsLayout.addWidget(backBtn)