import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QLabel

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
MENU_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "SANDWICH_MENU.png")
LOGO_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "logo.ico")
class Header(QWidget):
    def __init__(self, screen_width, screen_height, toggle_menu_callback):
        super().__init__()

        self. setContentsMargins(0, 0, 0, 0)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.setStyleSheet("background-color: white;")

        self.header_layout = QHBoxLayout(self)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Menu button
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon(MENU_ICON_PATH))
        self.menu_button.setToolTip("Toggle Menu")
        self.menu_button.clicked.connect(toggle_menu_callback)
        self.menu_button.setStyleSheet("border: none; background: transparent; padding: 0px;")

        # Logo
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap(LOGO_ICON_PATH)  # Adjust path to your logo file
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # self.logo_label.setMaximumSize(150,50)

        # self.header_label = QLabel("Header Section")
        self.header_label = QLabel("")
        self.header_label.setStyleSheet("color: black; font-size: 18px; padding-left: 10px;")

        # Add elements to header layout in swapped order
        # self.header_layout.addWidget(self.logo_label)  # Add logo first
        self.header_layout.addWidget(self.menu_button)  # Then add the menu button
        self.header_layout.addWidget(self.header_label)
        self.header_layout.addStretch()

        self.setMinimumHeight(int(self.screen_height * 0.08))
        self.setMaximumHeight(100)  # Set maximum height to 100 pixels

    def resizeEvent(self, event):
        """Adjust logo size on resize"""
        new_width = self.width()
        logo_size = int(new_width * 0.07)  # 10% of window width
        self.logo_label.setPixmap(
            self.logo_pixmap.scaled(logo_size, logo_size, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))

        icon_size = int(new_width * 0.05)  # Resize menu button icon size as well
        self.menu_button.setIconSize(QSize(icon_size, icon_size))

        super().resizeEvent(event)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Header(800, 600, lambda: print("Menu Toggled"))
    window.show()
    sys.exit(app.exec())
