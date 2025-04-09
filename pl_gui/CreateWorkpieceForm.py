import os
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QFrame,QSizePolicy, QSpacerItem,QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QWidget
from PyQt6.QtGui import QPixmap, QIcon
from .specific.enums.ToolID import ToolID
from .specific.enums.Gripper import Gripper
from .specific.enums.Program import Program
from .specific.enums.GlueType import GlueType
from .specific.enums.WorkpieceField import WorkpieceField
from enum import Enum

# Assuming the path to stylesheets
SETTINGS_STYLESHEET = os.path.join( "settings.qss")
TITLE = "Create Workpiece"
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

# Define paths for icons
WORKPIECE_ID_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "WOPIECE_ID_ICON_2.png")
WORKPIECE_NAME_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "WORKPIECE_NAME_ICON.png")
DESCRIPTION_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "DESCRIPTION_WORKPIECE_BUTTON_SQUARE.png")
OFFSET_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "OFFSET_VECTOR.png")
HEIGHT_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "HEIGHT_ICON.png")
TOOL_ID_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "TOOL_ID_ICON.png")
GRIPPER_ID_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "GRIPPER_ID_ICON.png")
GLUE_TYPE_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "GLUE_TYPE_ICON.png")
PROGRAM_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "PROGRAM_ICON.png")
MATERIAL_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "MATERIAL_ICON.png")
ACCEPT_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "ACCEPT_BUTTON.png")
CANCEL_BUTTON_ICON_PATH = os.path.join(RESOURCE_DIR, "createWorkpieceIcons", "CANCEL_BUTTON.png")

class CreateWorkpieceForm(QWidget):
    def __init__(self, parent=None, callBack=None):
        super().__init__(parent)
        #
        # try:
        #     with open(SETTINGS_STYLESHEET, "r") as file:
        #         app.setStyleSheet(file.read())
        # except FileNotFoundError:
        #     print("Stylesheet file not found. Using default styles.")

        self.onSubmitCallBack = callBack
        self.setWindowTitle(TITLE)
        self.setContentsMargins(0, 0, 0, 0)

        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.settingsLayout)

        self.icon_widgets = []  # To store icon widgets for resizing later

        self.addWidgets()

    def addWidgets(self):
        field_height = 40
        button_height = 50

        # Add widgets dynamically for workpiece form
        self.add_input_field(WorkpieceField.WORKPIECE_ID, "Enter Workpiece ID", WORKPIECE_ID_ICON_PATH)
        self.add_input_field(WorkpieceField.NAME, "Enter Workpiece Name", WORKPIECE_NAME_ICON_PATH)
        self.add_input_field(WorkpieceField.DESCRIPTION, "Enter Description", DESCRIPTION_ICON_PATH)
        self.add_input_field(WorkpieceField.OFFSET, "Enter Offset", OFFSET_ICON_PATH)
        self.add_input_field(WorkpieceField.HEIGHT, "Enter Workpiece Weight", HEIGHT_ICON_PATH)

        # Dropdown fields for Tool ID, Gripper ID, etc.
        self.add_dropdown_field(WorkpieceField.TOOL_ID, ToolID, TOOL_ID_ICON_PATH)
        self.add_dropdown_field(WorkpieceField.GRIPPER_ID, Gripper, GRIPPER_ID_ICON_PATH)
        self.add_dropdown_field(WorkpieceField.GLUE_TYPE, GlueType, GLUE_TYPE_ICON_PATH)
        self.add_dropdown_field(WorkpieceField.PROGRAM, Program, PROGRAM_ICON_PATH)

        # Add Material Type dropdown (manual list, replace with enums if needed)
        self.add_dropdown_field(WorkpieceField.MATERIAL, ["Material1", "Material2", "Material3"], MATERIAL_ICON_PATH)

        spacer = QSpacerItem(0, 150, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.settingsLayout.addItem(spacer)
        # Add button layout (Submit, Cancel)
        button_layout = QHBoxLayout()
        self.add_button("Accept", ACCEPT_BUTTON_ICON_PATH, button_layout)
        self.add_button("Cancel", CANCEL_BUTTON_ICON_PATH, button_layout)

        self.settingsLayout.addLayout(button_layout)

    def add_input_field(self, label, placeholder, icon_path):
        """ Helper method to add a label, icon, and input field """
        layout = QHBoxLayout()
        icon_label = self.create_icon_label(icon_path)
        layout.addWidget(icon_label)
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setMinimumHeight(40)
        layout.addWidget(input_field)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(layout)
        setattr(self, f"{label.value}_edit", input_field)  # Dynamic attribute
        print(f"{label.value}_edit")

    def add_dropdown_field(self, label, enum_class, icon_path):
        """ Helper method to add a dropdown (QComboBox) with enum items """
        layout = QHBoxLayout()
        icon_label = self.create_icon_label(icon_path)
        layout.addWidget(icon_label)
        dropdown = QComboBox()

        # Check if enum_class is an enum type
        if isinstance(enum_class, type) and issubclass(enum_class, Enum):
            # If it's an enum, get the names of the enum values
            dropdown.addItems([item.value for item in enum_class])
        else:
            # If it's a list of strings, add them directly
            dropdown.addItems(enum_class)

        dropdown.setMinimumHeight(40)
        layout.addWidget(dropdown)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(layout)
        setattr(self, f"{label.value}_combo", dropdown)  # Dynamic attribute
        print(f"{label.value}_combo")

    def add_button(self, button_type, icon_path, layout):
        """ Helper method to add a button with an icon and click functionality """
        button = QPushButton("")
        button.setIcon(QIcon(icon_path))
        button.setMinimumHeight(50)

        # Store references to the buttons
        if button_type == "Accept":
            self.submit_button = button  # Store reference to the submit button
            button.clicked.connect(self.onSubmit)
        else:
            self.cancel_button = button  # Store reference to the cancel button
            button.clicked.connect(self.onCancel)

        layout.addWidget(button)

    def onSubmit(self):

        # gett all atributes of the class
        for attr_name in dir(self):
            if attr_name.endswith("combo") or attr_name.endswith("edit"):
                # Split by "_"
                parts = attr_name.split("_")
                key = "_".join(parts[:-1]) # Join parts except the last one and convert to uppercase
                attr_type = parts[-1]  # The last part indicates the type
                print(f"key = {key}, type = {attr_type}")


        # """ Collect form data and submit it """
        data = {
            WorkpieceField.WORKPIECE_ID.value: getattr(self,WorkpieceField.WORKPIECE_ID.value+"_edit").text(),
            WorkpieceField.NAME.value: getattr(self,WorkpieceField.NAME.value+"_edit").text(),
            WorkpieceField.DESCRIPTION.value: getattr(self,WorkpieceField.DESCRIPTION.value+"_edit").text(),
            WorkpieceField.TOOL_ID.value: getattr(self,WorkpieceField.TOOL_ID.value+"_combo").currentText(),
            WorkpieceField.GRIPPER_ID.value: getattr(self,WorkpieceField.GRIPPER_ID.value+"_combo").currentText(),
            WorkpieceField.GLUE_TYPE.value: getattr(self,WorkpieceField.GLUE_TYPE.value+"_combo").currentText(),
            WorkpieceField.PROGRAM.value: getattr(self,WorkpieceField.PROGRAM.value+"_combo").currentText(),
            WorkpieceField.MATERIAL.value: getattr(self,WorkpieceField.MATERIAL.value+"_combo").currentText(),
            WorkpieceField.OFFSET.value: getattr(self,WorkpieceField.OFFSET.value+"_edit").text(),
            WorkpieceField.HEIGHT.value: getattr(self,WorkpieceField.HEIGHT.value+"_edit").text()
        }
        print("Collected Data:", data)
        if self.onSubmitCallBack:
            self.onSubmitCallBack(data)
        self.close()

    def onCancel(self):
        """ Cancel the operation and close the form """
        # if self.onSubmitCallBack:
        #     self.onSubmitCallBack()
        self.close()

    def create_icon_label(self, path, size=24):
        """ Create a label with an icon, scaled to a specific size """
        pixmap = QPixmap(path)
        label = QLabel()
        label.setPixmap(pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation))
        self.icon_widgets.append((label, pixmap))  # Store original pixmap for resizing
        return label

    def resizeEvent(self, event):
        """ Handle resizing of the window and icon sizes """
        super().resizeEvent(event)
        newWidth = self.parent().width()

        # Resize the icons in the labels
        for label, original_pixmap in self.icon_widgets:
            label.setPixmap(original_pixmap.scaled(int(newWidth * 0.02), int(newWidth * 0.02),
                                                   Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation))

        # Resize the icons in the buttons if they exist
        if hasattr(self, 'submit_button') and self.submit_button:
            button_icon_size = QSize(int(newWidth * 0.05), int(newWidth * 0.05))
            self.submit_button.setIconSize(button_icon_size)

        if hasattr(self, 'cancel_button') and self.cancel_button:
            button_icon_size = QSize(int(newWidth * 0.05), int(newWidth * 0.05))
            self.cancel_button.setIconSize(button_icon_size)

    def setHeigh(self,value):
        getattr(self,WorkpieceField.HEIGHT.value+"_edit").setText(str(value))

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    form = CreateWorkpieceForm()
    form.show()
    sys.exit(app.exec())
