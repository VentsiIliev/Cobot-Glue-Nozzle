from PyQt6.QtWidgets import QWidget, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame, QSizePolicy, QApplication
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QMouseEvent
from PyQt6.QtCore import Qt, QTimer
import numpy as np


class CameraFeed(QFrame):
    def __init__(self, updateCallback=None):
        super().__init__()

        self.updateCallback = updateCallback

        # Get the screen size (resolution of the primary screen) using QScreen
        # screen = QApplication.primaryScreen()
        # screen_size = screen.size()
        # screen_width = screen_size.width()
        # screen_height = screen_size.height()
        self.screen_size = (1280,720)
        screen_width = self.screen_size[0]
        screen_height = self.screen_size[1]

        # Set widget size (80% of screen) and max cap
        # self.setFixedSize(int(screen_width * 0.8), int(screen_height * 0.8))
        self.setFixedSize(screen_width, screen_height)
        self.setMaximumSize(1280, 720)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: transparent; border: none;")

        # Layout for the frame
        self.layout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Graphics view
        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setFixedSize(self.size())
        self.graphics_view.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.graphics_view.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.graphics_view.setContentsMargins(0, 0, 0, 0)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphics_view.setStyleSheet("border: none;")

        self.layout.addWidget(self.graphics_view)

        # Scene
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Feed control
        self.is_feed_paused = False
        self.clicked_points = []
        self.transformedPoints = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateCameraLabel)
        self.timer.start(100)

    def set_image(self, image):
        if isinstance(image, str):
            pixmap = QPixmap(image)
        elif isinstance(image, np.ndarray):
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
        else:
            print("Unsupported image type")
            return

        if pixmap.isNull():
            print("Failed to load image")
            return

        resized_pixmap = pixmap.scaled(self.size().width(), self.size().height(),
                                       Qt.AspectRatioMode.IgnoreAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)

        self.scene.clear()
        pixmap_item = QGraphicsPixmapItem(resized_pixmap)
        self.scene.addItem(pixmap_item)
        self.graphics_view.setScene(self.scene)

    def updateCameraLabel(self):
        if self.is_feed_paused:
            return

        try:
            frame = self.updateCallback()
            if frame is not None:
                self.set_image(frame)
        except Exception as e:
            print(f"Exception occurred: {e}")

    def pause_feed(self, static_image=None):
        self.is_feed_paused = True
        self.clicked_points.clear()

        if static_image is not None:
            if isinstance(static_image, str):
                pixmap = QPixmap(static_image)
            elif isinstance(static_image, np.ndarray):
                height, width, channel = static_image.shape
                bytes_per_line = 3 * width
                q_image = QImage(static_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
            else:
                raise TypeError("Unsupported image type")

            resized_pixmap = pixmap.scaled(self.size().width(), self.size().height(),
                                           Qt.AspectRatioMode.IgnoreAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
            self.scene.clear()
            pixmap_item = QGraphicsPixmapItem(resized_pixmap)
            self.scene.addItem(pixmap_item)
            self.graphics_view.setScene(self.scene)

    def resume_feed(self):
        self.is_feed_paused = False
        self.timer.start(100)
        print("Feed resumed.")
        return self.clicked_points

    def getClickedPoints(self):
        points = self.clicked_points
        self.clicked_points = []
        return points

    def mousePressEvent(self, event: QMouseEvent):
        originalSize = [1280, 720]
        displaySize = [self.size().width(), self.size().height()]
        scale_x = originalSize[0] / displaySize[0]
        scale_y = originalSize[1] / displaySize[1]
        print(f"scale_x: {scale_x}, scale_y: {scale_y}")

        click_x = event.position().x()
        click_y = event.position().y()

        print(f"Raw mouse clicked at position: ({click_x:.2f}, {click_y:.2f})")
        scaledPointX = click_x * scale_x
        scaledPointY = click_y * scale_y
        print(f"Scaled mouse clicked at position({scaledPointX:2f},{scaledPointY:2f})")
        self.clicked_points.append((click_x, click_y))
        self.transformedPoints.append((scaledPointX, scaledPointY))
        self.draw_lines()

    def draw_lines(self):
        if not self.scene.items():
            return

        if self.is_feed_paused:
            pixmap_item = self.scene.items()[0]
            pixmap = pixmap_item.pixmap()

            painter = QPainter(pixmap)
            painter.setPen(QPen(Qt.GlobalColor.red, 3))

            for i in range(1, len(self.clicked_points)):
                x1, y1 = int(self.clicked_points[i - 1][0]), int(self.clicked_points[i - 1][1])
                x2, y2 = int(self.clicked_points[i][0]), int(self.clicked_points[i][1])
                painter.drawLine(x1, y1, x2, y2)

            painter.end()
            pixmap_item.setPixmap(pixmap)
            self.graphics_view.viewport().update()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = CameraFeed()
    window.set_image("resources/pl_ui_icons/Background_&_Logo.png")
    window.show()
    sys.exit(app.exec())
