import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QLabel, QFrame

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
MENU_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "SANDWICH_MENU.png")
LOGO_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "logo.ico")
ON_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "POWER_ON_BUTTON.png")
OFF_ICON_PATH = os.path.join(RESOURCE_DIR, "pl_ui_icons", "POWER_OFF_BUTTON.png")


class Header(QFrame):
    def __init__(self, screen_width, screen_height, toggle_menu_callback):
        super().__init__()

        self.setContentsMargins(0, 0, 0, 0)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.setStyleSheet("background-color: white;")

        self.header_layout = QHBoxLayout(self)
        self.header_layout.setContentsMargins(10, 0, 10, 0)
        self.header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Menu button
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon(MENU_ICON_PATH))
        self.menu_button.setToolTip("Toggle Menu")
        self.menu_button.clicked.connect(toggle_menu_callback)
        self.menu_button.setStyleSheet("border: none; background: transparent; padding: 0px;")

        # Logo label (not shown now, but useful later)
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap(LOGO_ICON_PATH)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Header label
        self.header_label = QLabel("")
        self.header_label.setStyleSheet("color: black; font-size: 18px; padding-left: 10px;")

        # Left side
        self.header_layout.addWidget(self.menu_button)
        self.header_layout.addWidget(self.header_label)

        # Stretch to push right-side buttons
        self.header_layout.addStretch()

        # Right-side icon-only buttons
        self.power_on_button = QPushButton()
        self.power_on_button.setIcon(QIcon(ON_ICON_PATH))
        self.power_on_button.setToolTip("Power On")
        self.power_on_button.setStyleSheet("border: none; background: transparent; padding: 0px;")

        self.power_off_button = QPushButton()
        self.power_off_button.setIcon(QIcon(OFF_ICON_PATH))
        self.power_off_button.setToolTip("Power Off")
        self.power_off_button.setStyleSheet("border: none; background: transparent; padding: 0px;")

        self.header_layout.addWidget(self.power_on_button)
        self.header_layout.addWidget(self.power_off_button)

        self.setMinimumHeight(int(self.screen_height * 0.08))
        self.setMaximumHeight(100)

    def resizeEvent(self, event):
        """Adjust icon sizes on resize"""
        new_width = self.width()
        icon_size = int(new_width * 0.05)

        self.menu_button.setIconSize(QSize(icon_size, icon_size))
        self.power_on_button.setIconSize(QSize(icon_size, icon_size))
        self.power_off_button.setIconSize(QSize(icon_size, icon_size))

        logo_size = int(new_width * 0.07)
        self.logo_label.setPixmap(
            self.logo_pixmap.scaled(logo_size, logo_size, Qt.AspectRatioMode.KeepAspectRatio))

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    screen_size = app.primaryScreen().size()
    header = Header(screen_size.width(), screen_size.height(), lambda: print("Menu toggled"))
    header.show()
    app.exec()
