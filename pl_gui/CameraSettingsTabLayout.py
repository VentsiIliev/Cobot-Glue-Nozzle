from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QApplication, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from .PlSlider import PlSlider
import sys
import os

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
BACKGROUND = os.path.join(RESOURCE_DIR, "pl_ui_icons", "Background_&_Logo.png")


class CameraSettingsTabLayout(QVBoxLayout):
    """Handles layout and contents of the Camera Settings tab."""

    def __init__(self, parent_widget):
        super().__init__(parent_widget)

        # Add Index, Width & Height sliders
        self.addDimensionSliders()
    def addDimensionSliders(self):
        """Creates sliders for Index, Width & Height with proper labels and spacing."""

        # Index Slider Layout
        self.index_layout = QHBoxLayout()
        self.index_slider = PlSlider(label_text="Index")
        self.index_slider.slider.setRange(0, 10)  # Adjust range based on your needs
        self.index_slider.slider.setValue(5)  # Default value for index slider
        self.index_layout.addWidget(self.index_slider)

        # Width Slider Layout
        self.width_layout = QHBoxLayout()
        self.width_slider = PlSlider(label_text="Width")
        self.width_slider.slider.setRange(0, 1920)
        self.width_slider.slider.setValue(1280)
        self.width_layout.addWidget(self.width_slider)

        # Height Slider Layout
        self.height_layout = QHBoxLayout()
        self.height_slider = PlSlider(label_text="Height")
        self.height_slider.slider.setRange(0, 1080)
        self.height_slider.slider.setValue(720)
        self.height_layout.addWidget(self.height_slider)

        # Add layouts to the main layout
        self.addLayout(self.index_layout)
        self.addLayout(self.width_layout)
        self.addLayout(self.height_layout)

        # Set alignment of the layouts to left and top
        self.setAlignment(self.index_layout, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.setAlignment(self.width_layout, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.setAlignment(self.height_layout, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Set the overall layout to left and top alignment
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def updateValues(self, cameraSettings):
        self.index_slider.slider.setValue(cameraSettings.get_camera_index())
        self.width_slider.slider.setValue(cameraSettings.get_camera_width())
        self.height_slider.slider.setValue(cameraSettings.get_camera_height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Camera Settings Tab Layout")

    layout = CameraSettingsTabLayout(window)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec())
