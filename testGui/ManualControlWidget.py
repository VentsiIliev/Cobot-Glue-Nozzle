from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QSizePolicy,
    QApplication, QSpacerItem, QHBoxLayout, QSizePolicy
)


class ManualControlWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()  # Create main vertical layout

        # Create horizontal layout for Z axis
        z_layout = QHBoxLayout()
        self.btn_z_plus = QPushButton("Z+")
        self.btn_z_minus = QPushButton("Z-")

        # Customize buttons
        buttons = [self.btn_z_plus, self.btn_z_minus]
        for btn in buttons:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setMinimumSize(60, 60)
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #905BA9;
                    border-radius: 6px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #EEE;
                }
            """)

        # Add buttons with spacer in between
        z_layout.addWidget(self.btn_z_plus)
        z_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        z_layout.addWidget(self.btn_z_minus)

        # Create grid layout for X and Y axes
        control_layout = QGridLayout()
        control_layout.setSpacing(10)

        # Create buttons for X and Y axes
        self.btn_x_minus = QPushButton("X-")
        self.btn_x_plus = QPushButton("X+")
        self.btn_y_plus = QPushButton("Y+")
        self.btn_y_minus = QPushButton("Y-")

        # Customize X and Y buttons
        xy_buttons = [self.btn_x_minus, self.btn_x_plus, self.btn_y_plus, self.btn_y_minus]
        for btn in xy_buttons:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.setMinimumSize(60, 60)
            btn.setStyleSheet("""
                QPushButton {
                    border: 2px solid #905BA9;
                    border-radius: 6px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #EEE;
                }
            """)

        # Arrange X and Y buttons in a grid
        control_layout.addWidget(self.btn_y_plus, 0, 1)
        control_layout.addWidget(self.btn_x_minus, 1, 0)
        control_layout.addWidget(self.btn_x_plus, 1, 2)
        control_layout.addWidget(self.btn_y_minus, 2, 1)

        # Add spacers for symmetry
        control_layout.addItem(QSpacerItem(20, 20), 0, 0)
        control_layout.addItem(QSpacerItem(20, 20), 2, 0)
        control_layout.addItem(QSpacerItem(20, 20), 1, 3)

        # Add the Z layout and control layout to the main layout
        main_layout.addLayout(z_layout)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ManualControlWidget()
    window.setWindowTitle("Manual Robot Control")
    window.resize(300, 300)
    window.show()
    sys.exit(app.exec())
