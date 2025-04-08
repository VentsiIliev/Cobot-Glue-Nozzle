from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QSizePolicy, QSpacerItem
from PyQt6.QtCore import Qt
from PlSlider import PlSlider  # Assuming PlSlider is available from your previous code


class RobotSettingsTabLayout(QVBoxLayout):
    """Handles layout and contents of the Robot Settings tab."""

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        # Add Robot settings layout
        self.addRobotSettings()

    def addRobotSettings(self):
        """Creates sliders for Robot settings."""

        # Create vertical layout for sliders
        self.sliders_layout = QVBoxLayout()

        # Add sliders for velocity, acceleration, tool, and user
        self.addSliders()

        # Combine sliders layout into a horizontal layout
        self.horizontal_layout = QHBoxLayout()

        # Add the sliders layout
        self.horizontal_layout.addLayout(self.sliders_layout)

        # Set the alignment of the items to the top within their layout
        self.horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add combined layout to the main layout
        self.addLayout(self.horizontal_layout)

    def addSliders(self):
        """Creates sliders for Velocity, Acceleration, Tool, and User."""

        # Velocity Slider Layout
        self.vel_layout = QHBoxLayout()
        self.vel_slider = PlSlider(label_text="Velocity")
        self.vel_slider.slider.setRange(0, 100)  # Adjust the range as necessary
        self.vel_slider.slider.setValue(50)  # Default value for velocity slider
        self.vel_layout.addWidget(self.vel_slider)
        self.sliders_layout.addLayout(self.vel_layout)

        # Acceleration Slider Layout
        self.acc_layout = QHBoxLayout()
        self.acc_slider = PlSlider(label_text="Acceleration")
        self.acc_slider.slider.setRange(0, 100)  # Adjust the range as necessary
        self.acc_slider.slider.setValue(50)  # Default value for acceleration slider
        self.acc_layout.addWidget(self.acc_slider)
        self.sliders_layout.addLayout(self.acc_layout)

        # Tool Slider Layout
        self.tool_layout = QHBoxLayout()
        self.tool_slider = PlSlider(label_text="Tool")
        self.tool_slider.slider.setRange(0, 10)  # Adjust the range as necessary
        self.tool_slider.slider.setValue(5)  # Default value for tool slider
        self.tool_layout.addWidget(self.tool_slider)
        self.sliders_layout.addLayout(self.tool_layout)

        # User Slider Layout
        self.user_layout = QHBoxLayout()
        self.user_slider = PlSlider(label_text="User")
        self.user_slider.slider.setRange(0, 10)  # Adjust the range as necessary
        self.user_slider.slider.setValue(5)  # Default value for user slider
        self.user_layout.addWidget(self.user_slider)
        self.sliders_layout.addLayout(self.user_layout)

        # Set spacing between sliders
        self.sliders_layout.setSpacing(10)

        # Set alignment of sliders layout to top
        self.sliders_layout.setAlignment(Qt.AlignmentFlag.AlignTop)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Robot Settings Tab Layout")

    # Create and add Robot Settings tab layout
    robot_settings_tab_layout = RobotSettingsTabLayout(window)

    window.setLayout(robot_settings_tab_layout)
    window.show()

    sys.exit(app.exec())
