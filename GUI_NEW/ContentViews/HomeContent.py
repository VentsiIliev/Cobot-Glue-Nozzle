from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QMouseEvent
from PyQt6.QtCore import Qt, QTimer
import numpy as np
from API.Request import Request
from API.Response import Response
from API import Constants

class HomeContent(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.container = QWidget()
        self.container.setStyleSheet("background-color: red;")
        self.layout = QVBoxLayout(self.container)
        self.graphics_view = QGraphicsView(self)
        # self.graphics_view.setFixedSize(800, 450)
        self.graphics_view.setFixedSize(1280, 720)
        self.graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout.addWidget(self.graphics_view)
        self.setLayout(self.layout)

        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)

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

        # Resize the pixmap to 800x450
        # resized_pixmap = pixmap.scaled(800, 450, Qt.AspectRatioMode.KeepAspectRatio,
        #                                Qt.TransformationMode.SmoothTransformation)
        resized_pixmap = pixmap # new

        self.scene.clear()
        pixmap_item = QGraphicsPixmapItem(resized_pixmap)
        self.scene.addItem(pixmap_item)
        self.graphics_view.setScene(self.scene)

    def updateCameraLabel(self):
        if self.is_feed_paused:
            return

        try:
            request = Request(req_type=Constants.REQUEST_TYPE_GET,
                              action=Constants.CAMERA_ACTION_GET_LATEST_FRAME,
                              resource=Constants.REQUEST_RESOURCE_CAMERA)
            response = self.mainWindow.sendRequest(request)
            response = Response.from_dict(response)
            if response.status != Constants.RESPONSE_STATUS_SUCCESS:
                print("Error getting latest frame")
                return
            frame = response.data['frame']
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

            # resized_pixmap = pixmap.scaled(800, 450, Qt.AspectRatioMode.KeepAspectRatio,
            #                                Qt.TransformationMode.SmoothTransformation)
            resized_pixmap = pixmap # new
            # self.graphics_view.setFixedSize(800, 450)
            self.graphics_view.setFixedSize(1280, 720)
            self.scene.clear()
            pixmap_item = QGraphicsPixmapItem(resized_pixmap)
            self.scene.addItem(pixmap_item)
            self.graphics_view.setScene(self.scene)

    def resume_feed(self):
        # self.graphics_view.setFixedSize(800, 450)
        self.graphics_view.setFixedSize(1280, 720)
        self.is_feed_paused = False
        self.timer.start(100)
        print("Feed resumed.")
        return self.clicked_points

    def mousePressEvent(self, event: QMouseEvent):
        """Capture the mouse click event and get the raw coordinates (relative to the QGraphicsView)."""
        originalSize = [1280,720]
        # displaySize = [800,450]
        displaySize = [1280,720]
        scale_x = originalSize[0] / displaySize[0]
        scale_y = originalSize[1] / displaySize[1]
        print(f"scale_x: {scale_x}, scale_y: {scale_y}")
        # Get the raw mouse position relative to the QGraphicsView
        click_x = event.position().x() -10 # x coordinate relative to the QGraphicsView
        click_y = event.position().y() -126 # y coordinate relative to the QGraphicsView

        print(f"Raw mouse clicked at position: ({click_x:.2f}, {click_y:.2f})")
        scaledPointX = click_x * scale_x
        scaledPointY = click_y * scale_y
        self.clicked_points.append((click_x, click_y))  # Store the clicked point in raw coordinates
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

