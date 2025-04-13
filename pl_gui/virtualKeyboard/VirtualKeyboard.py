from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QGridLayout,
    QLineEdit, QApplication, QSizePolicy
)
from PyQt6.QtCore import Qt, QPoint
import sys


# ----- Virtual Keyboard Singleton -----
class VirtualKeyboardSingleton:
    __instance = None
    suppress_next_show = False

    @staticmethod
    def getInstance(target_input=None, parent=None) -> 'VirtualKeyboard':
        if VirtualKeyboardSingleton.__instance is None:
            VirtualKeyboardSingleton.__instance = VirtualKeyboard(target_input=target_input, parent=parent)
        elif target_input:
            VirtualKeyboardSingleton.__instance.update_target_input(target_input)
        return VirtualKeyboardSingleton.__instance

    @staticmethod
    def suppress_once():
        VirtualKeyboardSingleton.suppress_next_show = True

    @staticmethod
    def should_suppress():
        val = VirtualKeyboardSingleton.suppress_next_show
        VirtualKeyboardSingleton.suppress_next_show = False
        return val


# ----- Custom Input Field -----
class FocusLineEdit(QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)  # Call the superclass's __init__ method
        self.parent = parent  # Initialize the parent attribute

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if VirtualKeyboardSingleton.should_suppress():
            return
        keyboard = VirtualKeyboardSingleton.getInstance(self.parent)
        keyboard.update_target_input(self)
        keyboard.show()


# ----- Virtual Keyboard -----
class VirtualKeyboard(QWidget):
    def __init__(self, target_input=None, parent=None):
        super().__init__(parent)
        self.target_input = target_input

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)

        self.setMinimumSize(1000, 500)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.drag_position = QPoint()
        self.mode = 'letters'

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(2)  # Or 0 if you want *tight* layout

        self.layout.addLayout(self.grid_layout)

        hide_button = QPushButton("Hide Keyboard")
        hide_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        hide_button.clicked.connect(self.hideKeyboard)
        self.layout.addWidget(hide_button)

        self.key_buttons = []
        self.build_keyboard()
        self.apply_styles()

    def build_keyboard(self):
        for btn in self.key_buttons:
            btn.deleteLater()
        self.key_buttons.clear()
        self.grid_layout.setSpacing(10)

        # Always show number row
        number_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for col, key in enumerate(number_keys):
            button = QPushButton(key)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

            # button.setFixedSize(45, 45)
            button.clicked.connect(lambda _, k=key: self.key_pressed(k))
            self.key_buttons.append(button)
            self.grid_layout.addWidget(button, 0, col)

        # Define layout based on mode
        if self.mode in ['letters', 'shift']:
            keys = [
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                ['⇧', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '⌫'],
                ['SYM', 'space', '⏎']
            ]
            if self.mode == 'shift':
                keys = [[k.upper() if k not in ['⇧', '⌫', 'SYM', 'space', '⏎'] else k for k in row] for row in keys]
        elif self.mode == 'symbols':
            keys = [
                ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')'],
                ['_', '+', '=', '-', '/', ':', ';', '"', "'"],
                ['ABC', '\\', '|', '<', '>', '[', ']', '{', '}', '⌫'],
                ['.', ',', '⏎']
            ]

        # Add remaining keys
        for row_offset, row in enumerate(keys, start=1):
            for col, key in enumerate(row):
                button = QPushButton(key)
                # button.setFixedSize(45, 45)
                button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                button.clicked.connect(lambda _, k=key: self.key_pressed(k))
                self.key_buttons.append(button)
                self.grid_layout.addWidget(button, row_offset, col)

    def key_pressed(self, key):
        if not self.target_input:
            return
        if key == '⌫':
            self.target_input.backspace()
        elif key == '⏎':
            self.hideKeyboard()
        elif key == '⇧':
            self.mode = 'shift' if self.mode != 'shift' else 'letters'
            self.build_keyboard()
        elif key == 'SYM':
            self.mode = 'symbols'
            self.build_keyboard()
        elif key == 'ABC':
            self.mode = 'letters'
            self.build_keyboard()
        elif key == 'space':
            self.target_input.insert(' ')
        else:
            self.target_input.insert(key)
            if self.mode == 'shift':
                self.mode = 'letters'
                self.build_keyboard()

    def hideKeyboard(self):
        VirtualKeyboardSingleton.suppress_once()
        self.target_input.clearFocus()
        self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()

    def update_target_input(self, target_input):
        self.target_input = target_input

    def show(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        self.move((screen_geometry.width() - self.width()) // 2, 0)  # Centered horizontally, top of the screen
        super().show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        for btn in self.key_buttons:
            font = btn.font()
            btn_width = btn.width()
            font_size = max(10, btn_width // 6)  # Scale font to button width
            font.setPointSize(font_size)
            btn.setFont(font)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }

            QPushButton {
                background-color: white;
                color: #905BA9;
                border: 1px solid #905BA9;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:pressed {
                background-color: #905BA9;
                color: white;
            }

            QPushButton:hover {
                background-color: #905BA9;
                color: white
            }
        """)


# ----- Main Application -----
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QWidget()
    main_window.setStyleSheet("background-color: white;")
    main_window.setFixedSize(800, 600)

    input1 = FocusLineEdit(main_window)
    input1.setGeometry(50, 50, 300, 40)

    input2 = FocusLineEdit(main_window)
    input2.setGeometry(50, 120, 300, 40)

    input3 = FocusLineEdit(main_window)
    input3.setGeometry(50, 190, 300, 40)

    keyboard = VirtualKeyboardSingleton.getInstance(parent=main_window)

    main_window.show()
    sys.exit(app.exec())
