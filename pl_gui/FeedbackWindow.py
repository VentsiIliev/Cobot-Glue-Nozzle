from PyQt6.QtWidgets import (
    QApplication, QDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize


class FeedbackWindow(QDialog):
    def __init__(self, image_path, message_type="info"):
        super().__init__()

        self.setWindowTitle("Feedback")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.resize(360, 360)  # Good starting size
        self.setMinimumSize(280, 280)
        self.setMaximumSize(500, 500)  # Limit growth to avoid screen overflow
        # self.setStyleSheet("background:white;")
        self.setStyleSheet("background:#f5f5f5;")  # Very light gray
        # self.setStyleSheet("background:#fafafa;")  # Near white, soft gray tone

        # Icon paths
        icon_paths = {
            "info": "resources/pl_ui_icons/messages/DESCRIPTION_ICON.png",
            "warning": "resources/pl_ui_icons/messages/POP_UP_NOTIFICATION_ICON.png",
            "error": "resources/pl_ui_icons/messages/DESCRIPTION_ICON.png"
        }

        # === Top icon (left aligned)
        top_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_pixmap = QPixmap(icon_paths.get(message_type, icon_paths["info"]))
        icon_label.setPixmap(
            icon_pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(icon_label)
        top_layout.addStretch()

        # === Main image (scaled and size-capped)
        self.image_label = QLabel()
        self.original_pixmap = QPixmap(image_path)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_label.setMaximumSize(220, 220)
        self.image_label.setPixmap(self.original_pixmap.scaled(
            220, 220, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))

        # === OK button
        ok_button = QPushButton()
        ok_button.setIcon(QIcon("resources/pl_ui_icons/ACCEPT_BUTTON.png"))
        ok_button.setIconSize(QSize(64, 64))  # Slightly smaller
        ok_button.setStyleSheet("border:none;")
        ok_button.setFixedSize(64, 64)
        ok_button.clicked.connect(self.accept)

        # === Main layout
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def show_feedback(self):
        self.exec()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = FeedbackWindow(
        image_path="resources/pl_ui_icons/messages/MOVE_CALIBRATION_PATTERN.png",
        message_type="warning"
    )

    window2 = FeedbackWindow(
        image_path="resources/pl_ui_icons/messages/CAMERA_NOT_CALIBRATED.png",
        message_type="error"
    )
    window.show_feedback()
    window2.show_feedback()

    sys.exit(app.exec())
