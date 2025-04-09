import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDateEdit, QGridLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPixmap

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
PLACEHOLDER_IMAGE_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "placeholder.jpg")

class GalleryContent(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: white; padding: 20px;")
        self.layout = QVBoxLayout(self)

        # Date picker for filtering
        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate())
        self.layout.addWidget(self.date_picker)

        # Gallery grid layout
        self.gallery_layout = QGridLayout()
        self.gallery_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.gallery_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.gallery_layout)

        # Add placeholders with labels to the gallery
        for row in range(3):
            for col in range(6):
                placeholder_layout = QVBoxLayout()
                label = QLabel(f"Label {row * 3 + col + 1}")
                label.setStyleSheet("font-size: 14px; color: black; margin-bottom: 5px;")

                # Load image from local file
                placeholder = QLabel()
                pixmap = QPixmap(PLACEHOLDER_IMAGE_PATH)
                scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                placeholder.setPixmap(scaled_pixmap)
                placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
                placeholder.setStyleSheet("margin: 0px; text-align: left;")

                placeholder_layout.addWidget(label)
                placeholder_layout.addWidget(placeholder)
                placeholder_layout.setContentsMargins(0, 0, 0, 0)
                placeholder_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                self.gallery_layout.addLayout(placeholder_layout, row, col)

        # Add a spacer to push items to the top
        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = GalleryContent()
    window.show()
    sys.exit(app.exec())