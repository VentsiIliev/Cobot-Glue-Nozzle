import os
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QWidget
from PyQt6.QtGui import QPixmap, QIcon
from specific.enums.ToolID import ToolID
from specific.enums.Gripper import Gripper
from specific.enums.Program import Program
from specific.enums.GlueType import GlueType
from specific.enums.WorkpieceField import WorkpieceField
from enum import Enum


# Assuming the path to stylesheets
SETTINGS_STYLESHEET = os.path.join("GUI_NEW", "settings.qss")
TITLE = "Create Workpiece"


class CreateWorkpieceForm(QWidget):
    def __init__(self, parent=None, callBack=None):
        super().__init__(parent)
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
        self.add_input_field(WorkpieceField.WORKPIECE_ID, "Enter Workpiece ID", "resources/createWorkpieceIcons/WOPIECE_ID_ICON_2.png")
        self.add_input_field(WorkpieceField.NAME, "Enter Workpiece Name", "resources/createWorkpieceIcons/WORKPIECE_NAME_ICON.png")
        self.add_input_field(WorkpieceField.DESCRIPTION, "Enter Description", "resources/createWorkpieceIcons/DESCRIPTION_WORKPIECE_BUTTON_SQUARE.png")
        self.add_input_field(WorkpieceField.OFFSET, "Enter Offset", "resources/createWorkpieceIcons/OFFSET_VECTOR.png")
        self.add_input_field(WorkpieceField.HEIGHT, "Enter Workpiece Weight", "resources/createWorkpieceIcons/HEIGHT_ICON.png")

        # Dropdown fields for Tool ID, Gripper ID, etc.
        self.add_dropdown_field(WorkpieceField.TOOL_ID, ToolID, "resources/createWorkpieceIcons/TOOL_ID_ICON.png")
        self.add_dropdown_field(WorkpieceField.GRIPPER_ID, Gripper, "resources/createWorkpieceIcons/GRIPPER_ID_ICON.png")
        self.add_dropdown_field(WorkpieceField.GLUE_TYPE, GlueType, "resources/createWorkpieceIcons/GLUE_TYPE_ICON.png")
        self.add_dropdown_field(WorkpieceField.PROGRAM, Program, "resources/createWorkpieceIcons/PROGRAM_ICON.png")

        # Add Material Type dropdown (manual list, replace with enums if needed)
        self.add_dropdown_field(WorkpieceField.MATERIAL, ["Material1", "Material2", "Material3"], "resources/createWorkpieceIcons/MATERIAL_ICON.png")

        # Add button layout (Submit, Cancel)
        button_layout = QHBoxLayout()
        self.add_button("Accept", "resources/createWorkpieceIcons/ACCEPT_BUTTON.png", button_layout)
        self.add_button("Cancel", "resources/createWorkpieceIcons/CANCEL_BUTTON.png", button_layout)
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
        setattr(self, f"{label.lower().replace(' ', '_')}_edit", input_field)  # Dynamic attribute
        print(f"{label.lower().replace(' ', '_')}_edit")

    def add_dropdown_field(self, label, enum_class, icon_path):
        """ Helper method to add a dropdown (QComboBox) with enum items """
        layout = QHBoxLayout()
        icon_label = self.create_icon_label(icon_path)
        layout.addWidget(icon_label)
        dropdown = QComboBox()

        # Check if enum_class is an enum type
        if isinstance(enum_class, type) and issubclass(enum_class, Enum):
            # If it's an enum, get the names of the enum values
            dropdown.addItems([item.name for item in enum_class])
        else:
            # If it's a list of strings, add them directly
            dropdown.addItems(enum_class)

        dropdown.setMinimumHeight(40)
        layout.addWidget(dropdown)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(layout)
        setattr(self, f"{label.lower().replace(' ', '_')}_combo", dropdown)  # Dynamic attribute
        print(f"{label.lower().replace(' ', '_')}_combo")

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
            # Split by "_"
            parts = attr_name.split("_")
            key = "_".join(parts[:-1]).upper()  # Join parts except the last one and convert to uppercase
            attr_type = parts[-1]  # The last part indicates the type
            print(f"key = {key}, type = {attr_type}")
            # FIX ME !!!

        # """ Collect form data and submit it """
        # data = {
        #     WorkpieceField.WORKPIECE_ID: self.workpiece_id_edit.text().strip(),
        #     WorkpieceField.NAME: self.workpiece_name_edit.text().strip(),
        #     WorkpieceField.DESCRIPTION: self.description_edit.text().strip(),
        #     WorkpieceField.TOOL_ID: self.tool_id_combo.currentText().strip(),
        #     WorkpieceField.GRIPPER_ID: self.gripper_id_combo.currentText().strip(),
        #     WorkpieceField.GLUE_TYPE: self.glue_type_combo.currentText().strip(),
        #     WorkpieceField.PROGRAM: self.program_combo.currentText().strip(),
        #     WorkpieceField.MATERIAL: self.material_type_combo.currentText().strip(),
        #     WorkpieceField.OFFSET: self.offset_edit.text().strip(),
        #     WorkpieceField.HEIGHT: self.workpiece_height_edit.text().strip()
        # }
        # print("Collected Data:", data)
        # if self.onSubmitCallBack:
        #     self.onSubmitCallBack()
        # self.close()

    def onCancel(self):
        """ Cancel the operation and close the form """
        if self.onSubmitCallBack:
            self.onSubmitCallBack()
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


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    form = CreateWorkpieceForm()
    form.show()
    sys.exit(app.exec())
