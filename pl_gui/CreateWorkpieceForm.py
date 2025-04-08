from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

class CreateWorkpieceForm(QWidget):
    def __init__(self, parent=None, callBack=None):
        super().__init__(parent)
        self.onSubmitCallBack = callBack
        self.setWindowTitle("Create Workpiece Form")
        self.setContentsMargins(0, 0, 0, 0)
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.settingsLayout)
        self.icon_widgets = []  # Store original pixmaps

        self.addWidgets()

    def addWidgets(self):
        field_height = 40  # Set a higher height for fields for better touch interaction
        button_height = 50  # Set a height for buttons for better touch interaction

        # Add an icon and a line edit for Workpiece ID
        workpiece_id_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/WOPIECE_ID_ICON_2.png")
        workpiece_id_layout.addWidget(icon_label)
        self.workpiece_id_edit = QLineEdit()
        self.workpiece_id_edit.setPlaceholderText("Enter Workpiece ID")
        self.workpiece_id_edit.setMinimumHeight(field_height)
        workpiece_id_layout.addWidget(self.workpiece_id_edit)
        workpiece_id_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(workpiece_id_layout)

        # Add an icon and a line edit for Workpiece Name
        workpiece_name_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/WORKPIECE_NAME_ICON.png")
        workpiece_name_layout.addWidget(icon_label)
        self.workpiece_name_edit = QLineEdit()
        self.workpiece_name_edit.setPlaceholderText("Enter Workpiece Name")
        self.workpiece_name_edit.setMinimumHeight(field_height)
        workpiece_name_layout.addWidget(self.workpiece_name_edit)
        workpiece_name_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(workpiece_name_layout)

        # Add an icon and a line edit for Description
        description_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/DESCRIPTION_WORKPIECE_BUTTON_SQUARE.png")
        description_layout.addWidget(icon_label)
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Enter Description")
        self.description_edit.setMinimumHeight(field_height)
        description_layout.addWidget(self.description_edit)
        description_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(description_layout)

        # Add an icon and a combo box for Tool ID
        tool_id_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/TOOL_ID_ICON.png")
        tool_id_layout.addWidget(icon_label)
        self.tool_id_combo = QComboBox()
        self.tool_id_combo.addItems(["Tool1", "Tool2", "Tool3"])
        self.tool_id_combo.setMinimumHeight(field_height)
        tool_id_layout.addWidget(self.tool_id_combo)
        tool_id_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(tool_id_layout)

        # Add an icon and a combo box for Gripper ID
        gripper_id_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/GRIPPER_ID_ICON.png")
        gripper_id_layout.addWidget(icon_label)
        self.gripper_id_combo = QComboBox()
        self.gripper_id_combo.addItems(["Gripper1", "Gripper2", "Gripper3"])
        self.gripper_id_combo.setMinimumHeight(field_height)
        gripper_id_layout.addWidget(self.gripper_id_combo)
        gripper_id_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(gripper_id_layout)

        # Add an icon and a combo box for Glue Type
        glue_type_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/GLUE_TYPE_ICON.png")
        glue_type_layout.addWidget(icon_label)
        self.glue_type_combo = QComboBox()
        self.glue_type_combo.addItems(["Glue1", "Glue2", "Glue3"])
        self.glue_type_combo.setMinimumHeight(field_height)
        glue_type_layout.addWidget(self.glue_type_combo)
        glue_type_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(glue_type_layout)

        # Add an icon and a combo box for Program
        program_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/PROGRAM_ICON.png")
        program_layout.addWidget(icon_label)
        self.program_combo = QComboBox()
        self.program_combo.addItems(["Program1", "Program2", "Program3"])
        self.program_combo.setMinimumHeight(field_height)
        program_layout.addWidget(self.program_combo)
        program_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(program_layout)

        # Add an icon and a combo box for Material Type
        material_type_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/MATERIAL_ICON.png")
        material_type_layout.addWidget(icon_label)
        self.material_type_combo = QComboBox()
        self.material_type_combo.addItems(["Material1", "Material2", "Material3"])
        self.material_type_combo.setMinimumHeight(field_height)
        material_type_layout.addWidget(self.material_type_combo)
        material_type_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(material_type_layout)

        # Add an icon and a line edit for Offset
        offset_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/OFFSET_VECTOR.png")
        offset_layout.addWidget(icon_label)
        self.offset_edit = QLineEdit()
        self.offset_edit.setPlaceholderText("Enter Offset")
        self.offset_edit.setMinimumHeight(field_height)
        offset_layout.addWidget(self.offset_edit)
        offset_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(offset_layout)

        # Add an icon and a line edit for Workpiece Weight
        workpiece_weight_layout = QHBoxLayout()
        icon_label = self.create_icon_label("resources/createWorkpieceIcons/HEIGHT_ICON.png")
        workpiece_weight_layout.addWidget(icon_label)
        self.workpiece_weight_edit = QLineEdit()
        self.workpiece_weight_edit.setPlaceholderText("Enter Workpiece Weight")
        self.workpiece_weight_edit.setMinimumHeight(field_height)
        workpiece_weight_layout.addWidget(self.workpiece_weight_edit)
        workpiece_weight_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.settingsLayout.addLayout(workpiece_weight_layout)

        # Add a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Add a submit button with an icon
        self.submit_button = QPushButton("")
        self.submit_button.setIcon(
            QIcon("resources/createWorkpieceIcons/ACCEPT_BUTTON.png"))  # Replace with the actual path to your icon
        self.submit_button.setMinimumHeight(button_height)
        self.submit_button.clicked.connect(self.onSubmit)
        button_layout.addWidget(self.submit_button)

        # Add a cancel button with an icon
        self.cancelButton = QPushButton("")
        self.cancelButton.setIcon(QIcon("resources/createWorkpieceIcons/CANCEL_BUTTON.png"))  # Replace with the actual path to your icon
        self.cancelButton.setMinimumHeight(button_height)
        self.cancelButton.clicked.connect(self.onCancel)
        button_layout.addWidget(self.cancelButton)

        # Add the button layout to the main settings layout
        self.settingsLayout.addLayout(button_layout)

    def onCancel(self):
        self.onSubmitCallBack()
        self.close()

    def onSubmit(self):
        data = {
            "workpiece_id": self.workpiece_id_edit.text().strip(),
            "workpiece_name": self.workpiece_name_edit.text().strip(),
            "description": self.description_edit.text().strip(),
            "tool_id": self.tool_id_combo.currentText().strip(),
            "gripper_id": self.gripper_id_combo.currentText().strip(),
            "glue_type": self.glue_type_combo.currentText().strip(),
            "program": self.program_combo.currentText().strip(),
            "material_type": self.material_type_combo.currentText().strip(),
            "offset": self.offset_edit.text().strip(),
            "workpiece_weight": self.workpiece_weight_edit.text().strip()
        }

        # Print the collected data (or handle it as needed)
        print("Collected Data:", data)

        if self.onSubmitCallBack is not None:
            self.onSubmitCallBack()
        self.close()

    def create_icon_label(self, path, size=24):
        pixmap = QPixmap(path)
        label = QLabel()
        label.setPixmap(pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation))
        self.icon_widgets.append((label, pixmap))  # Store original pixmap for resizing
        return label

    def resizeEvent(self, event):
        super().resizeEvent(event)
        newWidth = self.parent().width()

        # Resize the icons in the labels
        for label, original_pixmap in self.icon_widgets:
            label.setPixmap(original_pixmap.scaled(int(newWidth*0.02), int(newWidth*0.02),
                                                   Qt.AspectRatioMode.KeepAspectRatio,
                                                   Qt.TransformationMode.SmoothTransformation))

        # Resize the icons in the buttons
        button_icon_size = QSize(int(newWidth*0.05), int(newWidth*0.05))
        self.submit_button.setIconSize(button_icon_size)
        self.cancelButton.setIconSize(button_icon_size)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    form = CreateWorkpieceForm()
    form.show()
    sys.exit(app.exec())
