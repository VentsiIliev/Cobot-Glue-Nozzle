import sys
import warnings
from PyQt6.QtWidgets import QApplication,QDialog, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize

# Suppress specific DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict() is deprecated")


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setGeometry(100, 100, 400, 400)  # Initial window size
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Set margins

        # Title Label
        self.label = QLabel("Login")
        self.label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.label.setStyleSheet("color: black;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        layout.addStretch(1)  # Push fields to the center

        # Username Input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("USERNAME")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            border-radius: 10px;
            border: 2px solid purple;
            color: black;
            text-transform: uppercase;
            font-size: 14px;
        }
        """)

        layout.addWidget(self.username_input)

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("PASSWORD")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("""
            border-radius: 10px;
            border: 2px solid purple;
            color: black;
            text-transform: uppercase;
            font-size: 14px;
        """)
        layout.addWidget(self.password_input)

        layout.addStretch(1)  # Push buttons to the bottom

        # Button Layout
        button_layout = QHBoxLayout()

        # Login Button
        self.login_button = QPushButton("")
        self.login_button.setIcon(QIcon("resources/pl_ui_icons/LOGIN_BUTTON_SQUARE.png"))
        self.login_button.setStyleSheet("border: none; background: transparent;")
        self.login_button.setSizePolicy(QPushButton().sizePolicy())  # Responsive
        self.login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_button)

        # QR Code Button
        self.qr_button = QPushButton("")
        self.qr_button.setIcon(QIcon("resources/pl_ui_icons/QR_CODE_BUTTON_SQUARE.png"))
        self.qr_button.setStyleSheet("border: none; background: transparent;")
        self.qr_button.setSizePolicy(QPushButton().sizePolicy())  # Responsive
        self.qr_button.clicked.connect(self.handle_qr_code)
        button_layout.addWidget(self.qr_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def resizeEvent(self, event):
        """Ensure buttons and icons stay large but within a reasonable size range."""
        new_width = self.width()
        new_height = self.height()

        # Button size: 50% of width, 15% of height (with min/max limits)
        button_width = max(160, min(int(new_width * 0.5), 300))  # Between 160px and 300px
        button_height = max(70, min(int(new_height * 0.15), 120))  # Between 70px and 120px

        # Icon size: 12% of width (with min/max limits)
        icon_size = QSize(max(60, min(int(new_width * 0.12), 100)),
                          max(60, min(int(new_width * 0.12), 100)))  # Between 60px and 100px

        self.login_button.setFixedSize(button_width, button_height)
        self.qr_button.setFixedSize(button_width, button_height)

        self.login_button.setIconSize(icon_size)
        self.qr_button.setIconSize(icon_size)

        super().resizeEvent(event)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        print(f"Login Attempt: {username} | {password}")  # Replace with actual login logic
        # TEMP: Accept everything, add real logic later
        if username and password:
            self.accept()  # <- closes the dialog with "Accepted"
        else:
            self.reject()  # optional, if you want to handle empty login

    def handle_qr_code(self):
        print("QR Code button clicked!")  # Implement QR scanning logic

    def mousePressEvent(self, event):
        """ Capture the position when the mouse is pressed. """
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """ Move the window when dragging. """
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        """ Stop dragging when mouse button is released. """
        self.dragging = False


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
