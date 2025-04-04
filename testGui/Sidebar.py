# ad imports
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class Sidebar(QWidget):
    def __init__(self, screen_width, upperButtonsConfigList, lowerButtonsConfigList=None):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.upperButtonsConfigList = upperButtonsConfigList
        self.lowerButtonsConfigList = lowerButtonsConfigList

        self.buttons = []
        self.screen_width = screen_width



        self.setStyleSheet("background-color: white; padding: 0px;")
        self.setFixedWidth(int(self.screen_width * 0.07))

        # Layout for sidebar
        self.sidebar_layout = QVBoxLayout(self)
        self.sidebar_layout.setSpacing(2)  # Adjust spacing here as needed
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        # Create all sidebar buttons
        self.create_sidebar_buttons()

    def create_sidebar_buttons(self):
        """Create all sidebar buttons and add them to the layout."""
        for config in self.upperButtonsConfigList:
            button = QPushButton()
            button.setCheckable(True)  # Enables toggle behavior
            button.setAutoExclusive(True)
            button.setIcon(QIcon(config.normalIconPath))
            button.normal_icon = config.normalIconPath  # Store normal icon
            button.pressed_icon = config.pressedIconPath  # Store pressed icon
            button.setToolTip(config.tooltip)
            button.clicked.connect(config.callback)
            button.toggled.connect(lambda checked, btn=button: self.update_icon(btn, checked))  # Change icon on toggle
            button.setStyleSheet("border: none; background: transparent; padding: 0px;")
            self.buttons.append(button)
            self.sidebar_layout.addWidget(button)

        self.sidebar_layout.addStretch()

        if self.lowerButtonsConfigList is None:
            return

        for config in self.lowerButtonsConfigList:
            button = QPushButton()
            button.setCheckable(True)  # Enables toggle behavior
            button.setAutoExclusive(True)
            button.setIcon(QIcon(config.normalIconPath))
            button.normal_icon = config.normalIconPath  # Store normal icon
            button.pressed_icon = config.pressedIconPath  # Store pressed icon
            button.setToolTip(config.tooltip)
            button.clicked.connect(config.callback)
            button.toggled.connect(lambda checked, btn=button: self.update_icon(btn, checked))  # Change icon on toggle
            button.setStyleSheet("border: none; background: transparent; padding: 0px;")
            self.buttons.append(button)
            self.sidebar_layout.addWidget(button)

    def update_icon(self, button, checked):
        """Update icon based on button's checked state."""
        if checked:
            button.setIcon(QIcon(button.pressed_icon))
        else:
            button.setIcon(QIcon(button.normal_icon))

    def update_button_states(self):
        """Ensure only one button remains checked at a time."""
        for button in self.buttons:
            if button.isChecked():
                button.setIcon(QIcon(button.pressed_icon))
            else:
                button.setIcon(QIcon(button.normal_icon))
                button.setChecked(False)  # Uncheck others

    def alignItemsLeft(self):
        for button in self.buttons:
            self.sidebar_layout.setAlignment(button, Qt.AlignmentFlag.AlignLeft)

    def alignItemsCenter(self):
        for button in self.buttons:
            self.sidebar_layout.setAlignment(button, Qt.AlignmentFlag.AlignCenter)
