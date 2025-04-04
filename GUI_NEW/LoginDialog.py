from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
# import QT
from PyQt6.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)

        if parent:
            print("Parent is not None")
            self.parent = parent
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
            parent_center = self.parent.geometry().center()
            self.move(parent_center.x() - self.width() // 2,
                      parent_center.y() - self.height() // 2)

        # load settings.qss and use them for the dialog
        try:
            self.setStyleSheet(open("GUI_NEW/sidebar.qss").read())
        except FileNotFoundError:
            print("Stylesheet not found")

        layout = QVBoxLayout()

        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.handle_login)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def handle_login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if username == "admin" and password == "password":
            # QMessageBox.information(self, "Success", "Login successful!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec():
        print("Logged in successfully")
    sys.exit(app.exec())
