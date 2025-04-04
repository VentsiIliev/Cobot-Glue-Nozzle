from PyQt6.QtWidgets import QLineEdit
# from GUI_NEW.virtualKeyboard.VirtualKeyboard import VirtualKeyboardSingleton
from GUI_NEW.virtualKeyboard.VirtualKeyboard import VirtualKeyboard
class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize the keyboard, passing the current CustomLineEdit as target_input
        # FIXME: VirtualKeyboardSingleton not working as expected when updating the target_input
        # self.keyboard = VirtualKeyboardSingleton.getInstance(target_input=self, parent=self)
        self.keyboard = VirtualKeyboard(target_input=self, parent=self)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        # Ensure keyboard shows up when this input field gains focus
        self.keyboard.show()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        # Optionally hide the keyboard when focus is lost
        self.keyboard.hide()
