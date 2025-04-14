import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt


class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)

        # This enforces a border at the QWidget level using QFrame
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(3)
        self.setStyleSheet("background-color: blue; border: 3px solid red;")

        layout = QVBoxLayout(self)
        for i in range(3):
            label = QLabel(f"Sidebar Item {i + 1}")
            label.setStyleSheet("padding: 10px; background-color: white;")
            layout.addWidget(label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sidebar with Forced Border")
        self.resize(800, 400)

        central = QWidget()
        layout = QHBoxLayout(central)

        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)

        main_content = QLabel("Main content area")
        main_content.setStyleSheet("background-color: #f0f0f0;")
        main_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(main_content, 1)

        self.setCentralWidget(central)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
