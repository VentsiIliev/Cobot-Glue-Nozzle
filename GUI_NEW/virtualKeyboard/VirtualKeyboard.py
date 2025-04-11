from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt, QPoint

class VirtualKeyboardSingleton:
    __instance = None

    @staticmethod
    def getInstance(target_input=None, parent=None) -> 'VirtualKeyboard':
        """Returns the single instance of VirtualKeyboard."""
        if VirtualKeyboardSingleton.__instance is None:
            VirtualKeyboardSingleton.__instance = VirtualKeyboard(target_input=target_input, parent=parent)
        elif target_input:  # Only update target_input if it’s passed
            # VirtualKeyboardSingleton.__instance.update_target_input(target_input) # FIXME: Not working as expected
            pass
        return VirtualKeyboardSingleton.__instance

class VirtualKeyboard(QWidget):
    def __init__(self, target_input=None, parent=None):
        super().__init__(parent)
        self.target_input = target_input

        # Inherit parent widget's style
        if parent:
            self.setStyleSheet(parent.styleSheet())  # Inherit the style from the parent

        # Remove close button (❌) and make it frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setFixedSize(500, 300)

        # Variables for dragging the window
        self.drag_position = QPoint()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Hide Keyboard Button
        hide_button = QPushButton("Hide Keyboard")
        hide_button.clicked.connect(self.hideKeyboard)
        layout.addWidget(hide_button)

        # Keyboard Layout
        grid_layout = QGridLayout()
        keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '←'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫', '⏎', '→']
        ]

        for row_index, row in enumerate(keys):
            for col_index, key in enumerate(row):
                button = QPushButton(key)
                button.clicked.connect(lambda checked, k=key: self.key_pressed(k))  # Corrected lambda issue
                button.setFixedSize(45, 45)  # Button size
                grid_layout.addWidget(button, row_index, col_index)

        layout.addLayout(grid_layout)

    def hideKeyboard(self):
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

    def key_pressed(self, key):
        if self.target_input:
            print(f"Key pressed: {key}")  # Debugging line to see if the method is called
            if key == "⌫":  # Backspace
                self.target_input.backspace()  # Removes the last character
            elif key == "⏎":  # Enter (Hide Keyboard)
                self.hideKeyboard()
            elif key == "→":  # Move Cursor Right
                cursor_pos = self.target_input.cursorPosition()
                self.target_input.setCursorPosition(cursor_pos + 1)
            elif key == "←":  # Move Cursor Left
                cursor_pos = self.target_input.cursorPosition()
                self.target_input.setCursorPosition(max(0, cursor_pos - 1))
            else:
                self.target_input.insert(key)  # Insert the character pressed

    def update_target_input(self, target_input):
        """Update the target input if needed."""
        self.target_input = target_input


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    # Create a main window to test the virtual keyboard
    main_window = QMainWindow()
    main_window.setWindowTitle("Virtual Keyboard Test")
    main_window.setFixedSize(800, 600)

    # Example input field
    input_field = QLineEdit(main_window)
    input_field.setGeometry(50, 50, 300, 40)

    # Initialize the virtual keyboard
    keyboard = VirtualKeyboardSingleton.getInstance(target_input=input_field, parent=main_window)

    main_window.show()
    sys.exit(app.exec())


