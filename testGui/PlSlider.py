from PyQt6.QtWidgets import QWidget, QSlider, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon


class PlSlider(QWidget):
    def __init__(self, orientation=Qt.Orientation.Horizontal, label_text="", parent=None):
        super().__init__(parent)

        self.setMaximumWidth(600)  # Example: Max width set to 400px
        self.setMaximumHeight(200)  # Example: Max height set to 100px

        # Initialize widgets
        self._initialize_widgets(orientation, label_text)

        # Set layout
        self._set_layout()

        # Connect signals
        self._connect_signals()

        # Set size policy to expand properly within layouts
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _initialize_widgets(self, orientation, label_text):
        """Initialize the widgets (slider, buttons, labels)"""
        # Create a label to describe the setting
        self.label = QLabel(label_text, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")

        # Create the slider
        self.slider = QSlider(orientation)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)
        self._set_slider_styles()

        # Create buttons to increase and decrease the value with icons
        self.minus_button = self._create_button("resources/pl_ui_icons/MINUS_BUTTON.png")  # Icon for minus
        self.plus_button = self._create_button("resources/pl_ui_icons/PLUS_BUTTON.png")    # Icon for plus

        # Value label to display current value of slider
        self.value_label = QLabel(str(self.slider.value()), self)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setFixedWidth(50)  # Adjust fixed width for better fit
        self.value_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")

    def _set_slider_styles(self):
        """Set the style for the slider"""
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #000000;
                height: 2px;
                background: #000000;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #905BA9;
                border: 1px solid #905BA9;
                width: 24px;
                height: 12px;
                margin: -5px 0;
                border-radius: 12px;
            }
            QSlider::sub-page:horizontal {
                background: #000000;
                border: 1px solid #000000;
                height: 4px;
                border-radius: 2px;
            }
            QSlider::add-page:horizontal {
                background: #000000;
                border: 1px solid #000000;
                height: 4px;
                border-radius: 2px;
        """)

    def _create_button(self, icon_path):
        """Helper function to create buttons with icons"""
        button = QPushButton()
        button.setIcon(QIcon(icon_path))  # Set the icon from the given path
        button.setIconSize(QSize(30, 30))  # Resize icon as needed
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Make button responsive
        button.setStyleSheet("""
            background-color: transparent;  /* Remove background */
            border: none; /* Remove the button border */
            border-radius: 25px; /* Round the button corners */
        """)
        return button

    def _set_layout(self):
        """Set the layout of the widgets"""
        # Vertical layout for the label
        self.label_layout = QVBoxLayout()
        self.label_layout.addWidget(self.label)

        # Horizontal layout for buttons, slider, and value label
        self.controls_layout = QHBoxLayout()
        self.controls_layout.addWidget(self.minus_button)
        self.controls_layout.addWidget(self.slider)
        self.controls_layout.addWidget(self.plus_button)
        self.controls_layout.addWidget(self.value_label)

        # Stretch the slider to take available space
        self.controls_layout.setStretch(1, 1)

        # Main horizontal layout to combine both layouts with a controlled spacer
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addStretch(1)  # Add spacer with stretch factor 1
        self.main_layout.addLayout(self.controls_layout)

    def _connect_signals(self):
        """Connect the signals (slider value change and button clicks)"""
        self.slider.valueChanged.connect(self.update_value_label)
        self.minus_button.clicked.connect(self.decrease_value)
        self.plus_button.clicked.connect(self.increase_value)

    def decrease_value(self):
        """Decrease the slider value"""
        value = self.slider.value()
        self.slider.setValue(value - 1)

    def increase_value(self):
        """Increase the slider value"""
        value = self.slider.value()
        self.slider.setValue(value + 1)

    def update_value_label(self):
        """Update the value label when slider value changes"""
        self.value_label.setText(str(self.slider.value()))

    def resizeEvent(self, event):
        """Adjust button sizes on resize event"""
        new_width = self.width()
        icon_size = int(new_width * 0.125)  # 5% of new window width
        self.minus_button.setIconSize(QSize(icon_size, icon_size))
        self.plus_button.setIconSize(QSize(icon_size, icon_size))
        super().resizeEvent(event)


# Application to display the slider
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("PlSlider Example")
    window_layout = QVBoxLayout(window)

    # Create and add slider widget
    slider = PlSlider(label_text="Volume")
    window_layout.addWidget(slider)

    window.show()
    sys.exit(app.exec())