from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QSizePolicy,
    QApplication, QSpacerItem, QHBoxLayout, QVBoxLayout
)
from PlSlider import PlSlider


class ManualControlWidget(QWidget):
    BASE_DIR = "resources/manualMoveIcons/"

    def __init__(self, parent=None,callback = None):
        super().__init__(parent)
        self.initUI()
        self.callback = callback

    def initUI(self):
        # Apply a single border around the entire widget (no internal borders)


        # Main layout (grid) for the entire widget
        main_layout = QGridLayout()
        main_layout.setSpacing(0)  # Reduce spacing inside the main layout
        main_layout.setContentsMargins(0, 0, 0, 0)  # No margins to avoid extra gaps

        # Create a new vertical layout to hold both Z and XY layouts together
        control_container_layout = QVBoxLayout()
        control_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        control_container_layout.setContentsMargins(0, 0, 0, 0)  # No inner margins
        control_container_layout.setSpacing(0)  # No spacing between inner widgets

        # Create a layout for the slider and align it to the center
        slider_layout = QHBoxLayout()
        slider_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider_layout.setContentsMargins(0, 0, 0, 0)  # No margins in slider layout
        slider_layout.setSpacing(0)  # No spacing between items in slider layout

        # Create the slider and add it to the slider layout
        slider = PlSlider(label_text="Step", parent=self)
        slider_layout.addWidget(slider)

        # Add the slider layout to the control container layout
        main_layout.addLayout(slider_layout, 0, 0)

        # Create horizontal layout for Z axis buttons
        z_layout = QHBoxLayout()
        z_layout.setSpacing(0)  # Zero spacing between buttons
        z_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        z_layout.setContentsMargins(0, 0, 0, 0)  # No margins for Z buttons

        self.btn_z_plus = QPushButton()
        self.btn_z_minus = QPushButton()

        # Set icons for Z buttons
        self.btn_z_plus.setIcon(QIcon(self.BASE_DIR + "Z+_BUTTON.png"))
        self.btn_z_minus.setIcon(QIcon(self.BASE_DIR + "Z-_BUTTON.png"))

        # Customize Z buttons
        for btn in [self.btn_z_plus, self.btn_z_minus]:
            btn.setFixedSize(60, 60)
            btn.setIconSize(QSize(40, 40))

        # Create timers for Z axis buttons
        self.z_plus_timer = QTimer(self)
        self.z_minus_timer = QTimer(self)
        self.z_plus_timer.setInterval(100)
        self.z_minus_timer.setInterval(100)

        # Connect timers to button actions
        self.btn_z_plus.pressed.connect(self.start_z_plus)
        self.btn_z_minus.pressed.connect(self.start_z_minus)
        self.btn_z_plus.released.connect(self.stop_z_plus)
        self.btn_z_minus.released.connect(self.stop_z_minus)

        self.z_plus_timer.timeout.connect(self.z_plus_action)
        self.z_minus_timer.timeout.connect(self.z_minus_action)

        # Add Z buttons to layout with no spacer in between
        z_layout.addWidget(self.btn_z_plus)
        z_layout.addWidget(self.btn_z_minus)

        # Create a grid layout for X and Y axis buttons (cross shape)
        cross_layout = QGridLayout()
        cross_layout.setSpacing(0)  # Zero spacing between buttons
        cross_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cross_layout.setContentsMargins(0, 0, 0, 0)  # No margins in cross layout

        # Create buttons for X and Y axes
        self.btn_x_minus = QPushButton()
        self.btn_x_plus = QPushButton()
        self.btn_y_plus = QPushButton()
        self.btn_y_minus = QPushButton()

        # Set icons for X and Y buttons
        self.btn_x_minus.setIcon(QIcon(self.BASE_DIR + "X-_BUTTON.png"))
        self.btn_y_minus.setIcon(QIcon(self.BASE_DIR + "Y-_BUTTON.png"))
        self.btn_x_plus.setIcon(QIcon(self.BASE_DIR + "X+_BUTTON.png"))
        self.btn_y_plus.setIcon(QIcon(self.BASE_DIR + "Y+_BUTTON.png"))

        # Customize X and Y buttons
        for btn in [self.btn_x_minus, self.btn_x_plus, self.btn_y_plus, self.btn_y_minus]:
            btn.setFixedSize(60, 60)
            btn.setIconSize(QSize(40, 40))

        # Create timers for X and Y buttons
        self.x_plus_timer = QTimer(self)
        self.x_minus_timer = QTimer(self)
        self.y_plus_timer = QTimer(self)
        self.y_minus_timer = QTimer(self)
        self.x_plus_timer.setInterval(100)
        self.x_minus_timer.setInterval(100)
        self.y_plus_timer.setInterval(100)
        self.y_minus_timer.setInterval(100)

        # Connect timers to button actions
        self.btn_x_plus.pressed.connect(self.start_x_plus)
        self.btn_x_minus.pressed.connect(self.start_x_minus)
        self.btn_y_plus.pressed.connect(self.start_y_plus)
        self.btn_y_minus.pressed.connect(self.start_y_minus)

        self.btn_x_plus.released.connect(self.stop_x_plus)
        self.btn_x_minus.released.connect(self.stop_x_minus)
        self.btn_y_plus.released.connect(self.stop_y_plus)
        self.btn_y_minus.released.connect(self.stop_y_minus)

        self.x_plus_timer.timeout.connect(self.x_plus_action)
        self.x_minus_timer.timeout.connect(self.x_minus_action)
        self.y_plus_timer.timeout.connect(self.y_plus_action)
        self.y_minus_timer.timeout.connect(self.y_minus_action)

        # Arrange the X and Y buttons in a grid (cross shape)
        cross_layout.addWidget(self.btn_x_minus, 0, 1)  # X- at (0, 1)
        cross_layout.addWidget(self.btn_y_minus, 1, 0)  # Y- at (1, 0)
        cross_layout.addWidget(self.btn_x_plus, 2, 1)  # X+ at (2, 1)
        cross_layout.addWidget(self.btn_y_plus, 1, 2)  # Y+ at (1, 2)
        # Add a spacer to the layout
        spacer = QSpacerItem(0, 10, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        cross_layout.addItem(spacer, 1, 1)  # Y+ at (1, 2)

        # Add Z layout and cross layout to the control container
        control_container_layout.addLayout(z_layout)
        control_container_layout.addLayout(cross_layout)
        control_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add control container layout to the main layout
        main_layout.addLayout(control_container_layout, 1, 0)

        # Add a spacer to the layout
        spacer = QSpacerItem(0, 300, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        main_layout.addItem(spacer)

        # Add close button to layout
        self.close_button = QPushButton("")
        self.close_button.setIcon(QIcon(self.BASE_DIR + "CANCEL_BUTTON.png"))
        main_layout.addWidget(self.close_button)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Set the main layout for the widget
        self.setLayout(main_layout)


    # Methods for starting/stopping timers for Z, X, Y buttons
    def start_z_plus(self): self.z_plus_timer.start()
    def stop_z_plus(self): self.z_plus_timer.stop()
    def start_z_minus(self): self.z_minus_timer.start()
    def stop_z_minus(self): self.z_minus_timer.stop()
    def start_x_plus(self): self.x_plus_timer.start()
    def stop_x_plus(self): self.x_plus_timer.stop()
    def start_x_minus(self): self.x_minus_timer.start()
    def stop_x_minus(self): self.x_minus_timer.stop()
    def start_y_plus(self): self.y_plus_timer.start()
    def stop_y_plus(self): self.y_plus_timer.stop()
    def start_y_minus(self): self.y_minus_timer.start()
    def stop_y_minus(self): self.y_minus_timer.stop()

    # Action methods for button presses
    def z_plus_action(self): print("Z+ Action triggered")
    def z_minus_action(self): print("Z- Action triggered")
    def x_plus_action(self): print("X+ Action triggered")
    def x_minus_action(self): print("X- Action triggered")
    def y_plus_action(self): print("Y+ Action triggered")
    def y_minus_action(self): print("Y- Action triggered")

    def resizeEvent(self, event):
        width = self.width()
        height = self.height()
        icon_size = min(width, height) // 8
        if width > 500:
            icon_size = min(width, height) // 8

        # Update icon sizes for buttons dynamically
        for btn in [self.btn_z_plus, self.btn_z_minus, self.btn_x_minus, self.btn_x_plus, self.btn_y_plus, self.btn_y_minus]:
            btn.setIconSize(QSize(icon_size, icon_size))
            btn.setFixedSize(QSize(icon_size, icon_size))

        newWidth = self.parent().width()
        button_icon_size = QSize(int(newWidth * 0.05), int(newWidth * 0.05))
        self.close_button.setIconSize(button_icon_size)
        self.close_button.clicked.connect(self.onClose)

        super().resizeEvent(event)


    def onClose(self):
        if self.callback is not None:
            self.callback()
        self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ManualControlWidget()
    window.setWindowTitle("Manual Robot Control")
    window.resize(300, 300)
    window.show()
    sys.exit(app.exec())
