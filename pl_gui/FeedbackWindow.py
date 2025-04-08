from PyQt6.QtWidgets import QApplication, QMessageBox, QPushButton
from PyQt6.QtCore import Qt


class FeedbackWindow(QMessageBox):
    def __init__(self, message, message_type="info"):
        super().__init__()

        self.setWindowTitle("Feedback")

        # Set message box type
        if message_type == "info":
            self.setIcon(QMessageBox.Icon.Information)
        elif message_type == "warning":
            self.setIcon(QMessageBox.Icon.Warning)
        elif message_type == "error":
            self.setIcon(QMessageBox.Icon.Critical)
        else:
            self.setIcon(QMessageBox.Icon.NoIcon)

        # Set the message text
        self.setText(message)

        # Add a custom button
        self.addButton(QPushButton("OK"), QMessageBox.ButtonRole.AcceptRole)

        # Adjust the size of the message box
        self.setStyleSheet("QMessageBox { font-size: 16px; }")

    def show_feedback(self):
        """ Show the feedback message box. """
        self.exec()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = FeedbackWindow(message="Calibration Successful!", message_type="info")
    window.show_feedback()
    sys.exit(app.exec())
