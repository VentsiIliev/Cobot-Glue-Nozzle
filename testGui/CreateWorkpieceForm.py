from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QWidget
from PyQt6.QtCore import Qt


class CreateWorkpieceForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Workpiece Form")
        self.setContentsMargins(0, 0, 0, 0)
        # self.setStyleSheet("background-color: white;")
        self.settingsLayout = QVBoxLayout()
        self.settingsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.settingsLayout)

        self.addWidgets()

    def addWidgets(self):
        # Add a label and a line edit for Workpiece ID
        workpiece_id_layout = QHBoxLayout()
        workpiece_id_layout.addWidget(QLabel("Workpiece ID"))
        self.workpiece_id_edit = QLineEdit()
        self.workpiece_id_edit.setPlaceholderText("Enter Workpiece ID")
        workpiece_id_layout.addWidget(self.workpiece_id_edit)
        self.settingsLayout.addLayout(workpiece_id_layout)

        # Add a label and a line edit for Workpiece Name
        workpiece_name_layout = QHBoxLayout()
        workpiece_name_layout.addWidget(QLabel("Workpiece Name"))
        self.workpiece_name_edit = QLineEdit()
        self.workpiece_name_edit.setPlaceholderText("Enter Workpiece Name")
        workpiece_name_layout.addWidget(self.workpiece_name_edit)
        self.settingsLayout.addLayout(workpiece_name_layout)

        # Add a label and a combo box for Tool ID
        tool_id_layout = QHBoxLayout()
        tool_id_layout.addWidget(QLabel("Tool ID"))
        self.tool_id_combo = QComboBox()
        self.tool_id_combo.addItems(["Tool1", "Tool2", "Tool3"])  # Add tool options
        tool_id_layout.addWidget(self.tool_id_combo)
        self.settingsLayout.addLayout(tool_id_layout)

        # Add a label and a combo box for Material Type
        material_type_layout = QHBoxLayout()
        material_type_layout.addWidget(QLabel("Material Type"))
        self.material_type_combo = QComboBox()
        self.material_type_combo.addItems(["Material1", "Material2", "Material3"])  # Add material options
        material_type_layout.addWidget(self.material_type_combo)
        self.settingsLayout.addLayout(material_type_layout)

        # Add a submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.onSubmit)
        self.settingsLayout.addWidget(self.submit_button)

    def onSubmit(self):
        # Handle the submit button click
        workpiece_id = self.workpiece_id_edit.text().strip()
        workpiece_name = self.workpiece_name_edit.text().strip()
        tool_id = self.tool_id_combo.currentText().strip()
        material_type = self.material_type_combo.currentText().strip()

        # Print the collected data (or handle it as needed)
        print(f"Workpiece ID: {workpiece_id}")
        print(f"Workpiece Name: {workpiece_name}")
        print(f"Tool ID: {tool_id}")
        print(f"Material Type: {material_type}")

        # You can add further processing or validation here

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    form = CreateWorkpieceForm()
    form.show()
    sys.exit(app.exec())