# settings_menu.py
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import Qt

import os

from GUI_NEW.customWidgets.CustomLineEdit import CustomLineEdit
from GUI_NEW.Enums import Widget
from API import Constants
from API.Request import Request

SETTINGS_STYLESHEET = os.path.join("GUI_NEW", "settings.qss")
TITLE = "Create Workpiece"


class CreateWorkpieceMenu(QFrame):
    """
      A PyQt6 GUI for creating a workpiece, which allows users to input details via dynamically generated fields.

      Attributes:
          parent: The parent widget that manages this form.
          config: A dictionary of configuration settings defining each field in the form.
    """

    def __init__(self, parent,
                 config):
        """
        Initializes the CreateWorkpieceMenu class and sets up the UI.

        Args:
            parent (QWidget): The parent widget that holds this settings menu.
            config (dict): A configuration dictionary that defines each field (e.g., widget type, default value, validation rules).

        Example:
            config = {
                WorkpieceField.WORKPIECE_ID: (Widget.LINE_EDIT, "", {"required": True, "is_numeric": True}),
                WorkpieceField.NAME: (Widget.LINE_EDIT, "", {"required": True, "is_numeric": False}),
                WorkpieceField.TOOL_ID: (Widget.DROPDOWN, [ToolID.Tool1.value, ToolID.Tool2.value], {"required": True, "is_numeric": False}),
                ...
            }
        """
        super().__init__()
        self.parent = parent
        self.config = config
        self.setFixedWidth(400)
        self.parent.load_stylesheet(self, SETTINGS_STYLESHEET)

        self.initUI()

    def initUI(self):
        """
        Initializes the user interface by setting up the layout and adding widgets dynamically.
        The widgets are based on the provided config dictionary, which specifies their type and default values.
        """
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.settingsLayout)

        settingsTitle = QLabel(TITLE)
        self.settingsLayout.addWidget(settingsTitle)
        self.addWidgets()

    def addWidgets(self):
        """
        Dynamically adds widgets (e.g., QLineEdit, QComboBox) based on the provided config.
        Each widget is given a label and added to the layout. Widgets can have default values
        and validation rules based on the config.

        This method also creates dynamically named attributes for each widget.
        """
        for key, configValue in self.config.items():
            self.settingsLayout.addWidget(QLabel((key.getAsLabel())))  # Ensure key is string
            widgetType, values, _ = configValue
            if widgetType == Widget.LINE_EDIT:
                attributeName = key.value + Widget.LINE_EDIT.value
                widget = CustomLineEdit()
                widget.setPlaceholderText(f"Enter {key.getAsLabel()}")
                widget.setText(values)
            elif widgetType == Widget.DROPDOWN:
                attributeName = key.value + Widget.DROPDOWN.value
                widget = QComboBox()
                widget.addItems(values if values else [])  # Add items if provided

            setattr(self, attributeName, widget)  # Dynamically create an attribute
            self.settingsLayout.addWidget(widget)  # Add widget to the layout

        # add submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.onSubmit)
        self.settingsLayout.addWidget(self.submit_button)

    def onSubmit(self):
        """
        Handles the submit button click. It collects the form data from dynamically created fields,
        validates it, and sends the data to a specified server or parent widget for processing.
        """
        print("Submit button clicked")

        # get all atributes that have been configuren in the addWidgets method
        formData = {}
        for key, configValue in self.config.items():
            widgetType, _, _ = configValue
            if widgetType == Widget.LINE_EDIT:
                attributeName = key.value + Widget.LINE_EDIT.value
            elif widgetType == Widget.DROPDOWN:
                attributeName = key.value + Widget.DROPDOWN.value
            else:
                raise ValueError(f"Unimplemented support for widget type: {widgetType}")

            widget = getattr(self, attributeName, None)  # Get the widget dynamically
            if widget:
                if widgetType == Widget.LINE_EDIT:
                    value = widget.text().strip() or None  # Get text from QLineEdit
                elif widgetType == Widget.DROPDOWN:
                    value = widget.currentText().strip() or None  # Get selected value from QComboBox
                else:
                    raise ValueError(f"Unimplemented support for widget type: {widgetType}")

                formData[key.value] = value  # Store value dynamically

        print("Collected Form Data:", formData)  # Debugging output

        # request = Request(Constants.REQUEST_TYPE_POST, Constants.REQUEST_ACTION_SAVE_WORKPIECE,
        #                   Constants.REQUEST_RESOURCE_WORKPIECE, data=formData)
        #
        # self.parent.sendRequest(request)
        self.parent.sendWorkpieceData(formData)
        # close the menu
        self.parent.close_create_workpiece()


    def validateData(self):
        """
        Validates the form data based on the validation rules defined in the config.

        It checks for the following:
        - Required fields (non-empty)
        - Numeric fields (valid numbers)

        Returns:
            Tuple: (Boolean indicating validity, String with validation result message)

        Example:
            validation_result, message = self.validateData()
            if not validation_result:
                self.showWarningMessage("Validation Error", message)
        """

        validated_data = {}

        for key, (widgetType, _, flags) in self.config.items():
            attributeName = key.value + (Widget.LINE_EDIT if widgetType == Widget.LINE_EDIT else Widget.DROPDOWN)
            widget = getattr(self, attributeName, None)

            if not widget:
                return False, f"Missing widget for {key.value}"

            # Retrieve value from widget
            value = widget.text().strip() if widgetType == Widget.LINE_EDIT else widget.currentText().strip()

            # Handle required field validation
            if flags.get("required", False) and not value:
                return False, f"{key.getAsLabel()} is required"

            # Handle numeric validation (if the flag is set)
            if flags.get("is_numeric", False):
                # Check if value is numeric or a valid float (including optional decimal point)
                if value and not value.replace(".", "", 1).isdigit():
                    try:
                        # Check for float values like 12.34 or .45
                        float(value)
                    except ValueError:
                        return False, f"{key.getAsLabel()} must be a valid number"

            validated_data[key.value] = value

        return True, "Data is valid"
