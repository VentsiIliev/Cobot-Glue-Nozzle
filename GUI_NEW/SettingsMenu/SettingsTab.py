# camera_tab.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QTabWidget, QLabel, QCheckBox, QLineEdit, QPushButton
from PyQt6.QtCore import Qt

from API.Response import Response
from API import Constants
from API.Request import Request
from API.shared.settings.BaseSettings import Settings
from GUI_NEW.Enums import Widget
from GUI_NEW.customWidgets.CustomLineEdit import CustomLineEdit
from PyQt6.QtGui import QInputMethod
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QMessageBox


class SettingsTab(QFrame):
    """
        A dynamic settings tab that allows modification and saving of settings for different configurations
        inheriting from BaseSettings.Settings.

        This class generates UI elements based on a configuration list containing settings objects and UI definitions.
        It supports different widget types (QLineEdit, QCheckBox) and dynamically creates attributes for them.

        Attributes:
            config (list): List of tuples containing (Settings object, tab configuration, settings key enum).
            mainWindow: Reference to the main application window.
            subTabs (QTabWidget): Container for multiple settings tabs.

        Example Configuration:
            ```python
            config = [
                (
                    SomeSettingsClass(),
                    {
                        "header": "General Settings",
                        SomeEnum.SETTING_1: (Widget.LINE_EDIT, {"type": str}),
                        SomeEnum.SETTING_2: (Widget.CHECKBOX, {"type": bool}),
                    },
                    SomeEnum
                )
            ]
            settings_tab = SettingsTab(mainWindow, config)
            ```
        """
    def __init__(self, mainWindow, config):
        for conf in config:
            if not isinstance(conf[0], Settings):
                raise TypeError("settingsClass must be a subclass of BaseSettings")
        super().__init__()
        self.config=config
        self.mainWindow = mainWindow
        try:
            self.mainWindow.load_stylesheet(self, "GUI_NEW/settings.qss")
            print("Loaded stylesheet")
        except:
            print("Error loading stylesheet")

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.subTabs = QTabWidget()
        self.createSettingsTabs()

        layout.addWidget(self.subTabs)

    def createSettingsTabs(self):
        """
            Dynamically creates tabs based on the provided configuration.
            Each setting is represented by a corresponding UI widget.
            """
        for conf in self.config:
            settingsObj = conf[0] # Settings object that hold the actual settings
            tabConf = conf[1] # Configuration for the tab eg. widget type, flags(is_numeric, type)

            # remove the header from the tabConf temporarily and set it as the tab header
            # in order to avoid issues when iterating over the tabConf
            header = tabConf.pop("header", "Settings")

            tabFrame = QFrame()
            layout = QVBoxLayout()
            tabFrame.setLayout(layout)


            for key, (widgetType, flags) in tabConf.items():

                # Use the enum getAsLabel method to get the label
                layout.addWidget(QLabel(key.getAsLabel()))
                if widgetType == Widget.LINE_EDIT:
                    # Create the attribute name by concatenating the key value and the widget type
                    attributeName = key.value + Widget.LINE_EDIT.value
                    # widget = QLineEdit()
                    widget = CustomLineEdit()
                    # Set the text of the widget to the value of the settings object
                    widget.setText(str(settingsObj.get_value(key.value)))
                elif widgetType == Widget.CHECKBOX:
                    # Create the attribute name by concatenating the key value and the widget type
                    attributeName = key.value + Widget.CHECKBOX.value
                    widget = QCheckBox()
                    # Set the checked state of the widget to the value of the settings object
                    widget.setChecked(settingsObj.get_value(key.value))
                    print(f"Checkbox value of {attributeName}: {widget.isChecked()}")
                else:
                    raise ValueError("Not implemented support for widget type: ", widgetType)
                # Dynamically create an attribute eg. self.keyLineEdit or self.keyCheckbox
                setattr(self, attributeName, widget)
                # Add the widget to the layout
                layout.addWidget(widget)
            # Add the header back to the tabConf
            tabConf["header"] = header

            # Save Button
            save_btn = QPushButton("Save Settings")
            save_btn.clicked.connect(self.saveSettings)
            layout.addWidget(save_btn)

            self.subTabs.addTab(tabFrame, header)



    def saveSettings(self):
        """
                Saves the settings for the currently selected tab.
                Iterates over the configuration, retrieves values from UI elements, and sends an update request.
                """
        # get the currently selected tab text/label
        currentTabText = self.subTabs.tabText(self.subTabs.currentIndex())
        tabConfig = None
        settingsObj = None
        settingsKeyEnum = None
        for conf in self.config:
            header = conf[1]['header']
            if currentTabText == header:
                tabConfig = conf[1] # Configuration for the tab eg. widget type, flags(is_numeric, type)
                settingsObject = conf[0] # Settings object that hold the actual settings
                settingsKeyEnum = conf[2] # Enum class that holds the keys for the settings
                break

        if tabConfig is None or settingsObject is None:
            raise ValueError("Tab not found")

        header = tabConfig.pop("header") # Remove the header from the tabConfig
        for key,(widgetType,flags) in tabConfig.items():
            expectedType = flags["type"] # Get the expected type from the flags eg. int, float, str etc.
            if widgetType == Widget.LINE_EDIT:
                # Create the attribute name by concatenating the key value and the widget type
                attributeName = key.value + Widget.LINE_EDIT.value
                # Get the widget by dynamically creating the attribute name
                widget = getattr(self,attributeName)
                # Get the input value from the widget
                value = widget.text()

                # If expected type is not a string, convert the value to the expected type
                if expectedType != str:
                    value = expectedType(float(value))


            elif widgetType == Widget.CHECKBOX:
                # same step as above
                attributeName = key.value + Widget.CHECKBOX.value
                widget = getattr(self,attributeName)
                value = widget.isChecked()
            else:
                raise ValueError("Not implemented support for widget type: ",widgetType)

            # Update the settings object with the new value
            settingsObject.set_value(key.value, value)

        # Add the header back to the tabConfig
        tabConfig["header"] = header

        # Create a dictionary to hold the settings
        settings = {
            "header":header
        }
        # Iterate over the enum keys and get the value from the settings object
        # and add it to the settings dictionary
        for enumKey in settingsKeyEnum:
            settings[enumKey.value] = settingsObject.get_value(enumKey.value)
            print(f"Settings: {enumKey.value} = {settingsObject.get_value(enumKey.value)}")

        # Create a request object with the settings dictionary
        request = Request(Constants.REQUEST_TYPE_POST, Constants.ACTION_SET_SETTINGS, settings.get('header'), settings)
        response = self.mainWindow.sendRequest(request)
        response = Response.from_dict(response)

        if response.status == Constants.RESPONSE_STATUS_SUCCESS:
            QMessageBox.information(self, "Success", response.message)
        else:
            QMessageBox.critical(self, response.message)

