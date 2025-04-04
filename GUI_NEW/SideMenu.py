# sidebar.py
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QFrame, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
import os

LOGO_PATH = "GUI_NEW/resources/logo.ico"

SIDE_MENU_STYLESHEET = os.path.join("GUI_NEW", "sidebar.qss")
HOME_ICON_PATH = "GUI_NEW/resources/icons/cil-home.png"
SETTINGS_ICON_PATH = "GUI_NEW/resources/icons/icon_settings.png"

class SideMenu(QFrame):
    def __init__(self, parent:'MainWindow',width:int,title:str):
        super().__init__()
        self.parent = parent
        self.title = title
        self.width = width

        self.setFixedWidth(self.width)
        self.parent.load_stylesheet(self, SIDE_MENU_STYLESHEET)
        self.initUI()


    def initUI(self):
        self.sidebarLayout = QVBoxLayout()
        self.sidebarLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.sidebarLayout)

        titleLayout = QHBoxLayout()
        logo = QLabel()
        logo.setPixmap(QPixmap(LOGO_PATH).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        titleLayout.addWidget(logo)
        title = QLabel(self.title)
        titleLayout.addWidget(title)
        self.sidebarLayout.addLayout(titleLayout)

    def addSpacer(self):
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.sidebarLayout.addItem(spacer)

    def setButtons(self,buttonsConfig):
        for config in buttonsConfig:
            self.__registerButton(config)

    def __registerButton(self,btnConfig):
        text,command,icon_path = btnConfig
        btn = QPushButton(text)
        btn.setIcon(QIcon(icon_path))
        btn.setCheckable(True)
        setattr(self, f"{text.replace(' ', '_').lower()}Btn", btn)
        btn.clicked.connect(command)
        self.sidebarLayout.addWidget(btn)

