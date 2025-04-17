import numpy as np
from PyQt6.QtCore import Qt, QPointF, pyqtSignal, QEvent, QTimer
from PyQt6.QtGui import QPainter,QImage, QPen, QBrush, QPainterPath
from PyQt6.QtWidgets import QFrame,QPinchGesture,QApplication
import sys
from matplotlib import pyplot as plt

from contour_to_bezier import contour_to_bezier
from BezierSegmentManager import BezierSegmentManager


class ContourEditor(QFrame):
    pointsUpdated = pyqtSignal()

    def __init__(self, visionSystem, image_path=None,contours=None):
        super().__init__()
        self.setWindowTitle("Editable Bezier Curves")
        self.setGeometry(100, 100, 1280, 720)
        self.visionSystem = visionSystem
        self.manager = BezierSegmentManager()
        self.dragging_point = None

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self.setAutoFillBackground(False)
        self.image = self.load_image(image_path)
        self.selected_point_info = None

        self.scale_factor = 1.0
        self.translation = QPointF(0, 0)
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.is_zooming = False

        self.initContour(contours)

    def initContour(self,contours):
        if contours is not None:
            self.contours = contours
            for cnt in contours:

                bezier_segments = contour_to_bezier(cnt)  # List of dicts: {'points': [...], 'controls': [...]}
                for segment in bezier_segments:
                    self.manager.segments.append(segment)
                self.pointsUpdated.emit()

    def toggle_zooming(self):
        self.is_zooming = not self.is_zooming
        if self.is_zooming:
            self.grabGesture(Qt.GestureType.PinchGesture)
            print("Zooming and pinch gesture enabled.")
        else:
            self.ungrabGesture(Qt.GestureType.PinchGesture)
            print("Zooming and pinch gesture disabled.")
    def reset_zoom_flag(self):
        self.is_zooming = False

    def load_image(self, path):
        if path:
            image = QImage(path)
            if image.isNull():
                print(f"Failed to load image from: {path}")
                image = QImage(1280, 720, QImage.Format.Format_RGB32)
        else:
            image = QImage(1280, 720, QImage.Format.Format_RGB32)
        image.fill(Qt.GlobalColor.white)
        return image

    def handle_gesture_event(self, event):
        gesture = event.gesture(Qt.GestureType.PinchGesture)
        if gesture:
            pinch = gesture
            scale_factor = pinch.scaleFactor()
            center = pinch.centerPoint()  # Midpoint of the fingers

            # Map the center point to image space
            center_img_space = (center - self.translation) / self.scale_factor

            # Apply zoom factor
            self.scale_factor *= scale_factor

            # Adjust the translation to zoom towards the center of the pinch
            new_center_screen_pos = center_img_space * self.scale_factor + self.translation
            self.translation += center - new_center_screen_pos

            # Redraw the UI with the updated zoom and pan transformations
            self.update()

    def update_image(self, image_input):
        if isinstance(image_input, str):
            image = QImage(image_input)
            if image.isNull():
                print(f"Failed to load image from path: {image_input}")
                return
            self.image = image
        elif isinstance(image_input, QImage):
            self.image = image_input
        else:
            print("Unsupported image input type.")
            return
        self.update()

    def event(self, event):
        if event.type() == QEvent.Type.Gesture:
            self.handle_gesture_event(event)
            return True
        return super().event(event)



    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        factor = 1.25 if angle > 0 else 0.8

        cursor_pos = event.position()
        cursor_img_pos = (cursor_pos - self.translation) / self.scale_factor

        self.scale_factor *= factor

        # Update translation to zoom towards cursor
        new_cursor_screen_pos = cursor_img_pos * self.scale_factor + self.translation
        self.translation += cursor_pos - new_cursor_screen_pos

        self.update()

    def mousePressEvent(self, event):
        # Skip point placement if zooming is in progress
        if self.is_zooming:
            self.last_drag_pos = event.position()  # Store the position where drag started
            return

        if not self.is_within_image(event.position()):
            return  # Ignore clicks outside the image

        pos = self.map_to_image_space(event.position())

        if event.button() == Qt.MouseButton.RightButton:
            if self.manager.remove_control_point_at(pos):
                self.selected_point_info = None  # Deselect on right-click delete
                self.update()
                self.pointsUpdated.emit()
                return

        elif event.button() == Qt.MouseButton.LeftButton:
            drag_target = self.manager.find_drag_target(pos)
            if drag_target:
                self.dragging_point = drag_target
                self.selected_point_info = drag_target  # Mark it as selected
                self.initial_drag_pos = pos  # Store initial position where drag started
                self.update()
                return

            # Only add a point if we are NOT zooming
            self.manager.add_point(pos)
            self.selected_point_info = None  # Deselect if we just added a new one
            self.update()
            self.pointsUpdated.emit()

    def mouseDoubleClickEvent(self, event):
        pos = event.position()
        target = self.manager.find_drag_target(pos)

        if target and target[0] == 'control':
            role, seg_index, ctrl_idx = target
            self.manager.reset_control_point(seg_index, ctrl_idx)
            self.update()
            self.pointsUpdated.emit()

    def mouseMoveEvent(self, event):
        if self.dragging_point:
            # Get current position in image space
            current_pos = self.map_to_image_space(event.position())

            if not self.is_within_image(event.position()):
                return

            # Calculate delta movement
            delta = current_pos - self.initial_drag_pos

            # Extract the role, segment, and index of the point to be moved
            role, seg_index, idx = self.dragging_point

            # Move the point in the manager, considering delta movement
            self.manager.move_point(role, seg_index, idx, self.initial_drag_pos + delta)

            # Update the canvas to reflect the changes
            self.update()
            self.pointsUpdated.emit()  # Emit update to notify others of the change

            # Update initial position for the next movement
            self.initial_drag_pos = current_pos

    def mouseReleaseEvent(self, event):
        self.dragging_point = None

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_N:
            print("New segment started.")
            self.manager.start_new_segment()
            print("Current segments:", self.manager.get_segments())  # Debug print
            self.update()
            self.pointsUpdated.emit()

        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.save_robot_path_to_txt("robot_path.txt", samples_per_segment=5)
            self.plot_robot_path()
            import testTransformPoints  # External logic
        elif key == Qt.Key.Key_Space:
            print("Capturing image from vision system...")
            image = self.visionSystem.captureImage()
            contours = self.visionSystem.contours

            if image is None:
                print("Image capture failed.")
                return


            self.initContour(contours)

            height, width, channels = image.shape
            bytes_per_line = channels * width
            fmt = QImage.Format.Format_RGB888 if channels == 3 else QImage.Format.Format_RGBA888
            qimage = QImage(image.data, width, height, bytes_per_line, fmt)
            self.update_image(qimage)

    def map_to_image_space(self, pos):
        return (pos - self.translation) / self.scale_factor

    def paintEvent(self, event):
        painter = QPainter(self)
        if not painter.isActive():
            return

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), Qt.GlobalColor.white)

        # Apply transformation
        painter.translate(self.translation)
        painter.scale(self.scale_factor, self.scale_factor)

        painter.drawImage(0, 0, self.image)

        for segment in self.manager.get_segments():
            if segment.get("visible",True): # Default to True if missing
                self.draw_bezier_segment(painter, segment)

        painter.end()

    def draw_bezier_segment(self, painter, segment):
        points = segment['points']
        controls = segment['controls']
        if len(points) >= 2:
            path = QPainterPath()
            path.moveTo(points[0])
            for i in range(1, len(points)):
                if i - 1 < len(controls):
                    path.quadTo(controls[i - 1], points[i])
            painter.setPen(QPen(Qt.GlobalColor.black, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)

        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(QBrush(Qt.GlobalColor.blue))
        for i, pt in enumerate(points):
            is_selected = (
                    self.selected_point_info == ('anchor', self.manager.segments.index(segment), i)
            )
            color = Qt.GlobalColor.green if is_selected else Qt.GlobalColor.blue
            size = 8 if is_selected else 5
            painter.setBrush(QBrush(color))
            painter.drawEllipse(pt, size, size)

        for i, pt in enumerate(controls):
            is_selected = (
                    self.selected_point_info == ('control', self.manager.segments.index(segment), i)
            )
            color = Qt.GlobalColor.green if is_selected else Qt.GlobalColor.red
            size = 8 if is_selected else 5
            painter.setBrush(QBrush(color))
            painter.drawEllipse(pt, size, size)

        painter.setPen(QPen(Qt.GlobalColor.gray, 1, Qt.PenStyle.DashLine))
        for i in range(1, len(points)):
            if i - 1 < len(controls):
                painter.drawLine(points[i - 1], controls[i - 1])
                painter.drawLine(controls[i - 1], points[i])

    def save_robot_path_to_txt(self, filename="robot_path.txt", samples_per_segment=5):
        path = self.manager.get_robot_path(samples_per_segment)
        try:
            with open(filename, 'w') as f:
                for pt in path:
                    f.write(f"{pt.x():.3f}, {pt.y():.3f}\n")
            print(f"Saved path to {filename}")
        except Exception as e:
            print(f"Error saving path: {e}")

    def plot_robot_path(self, filename="robot_path.txt"):
        try:
            with open(filename, 'r') as f:
                coords = [line.strip().split(',') for line in f if ',' in line]
            x_vals, y_vals = zip(*[(float(x), float(y)) for x, y in coords])
            plt.figure(figsize=(12.8, 7.2))
            plt.plot(x_vals, y_vals, 'b-', label="Robot Path")
            plt.gca().invert_yaxis()
            plt.xlim(0, self.width())
            plt.ylim(self.height(), 0)
            plt.title("Robot Path Visualization")
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Failed to plot path: {e}")

    def is_within_image(self, pos: QPointF) -> bool:
        image_width = self.image.width()
        image_height = self.image.height()
        img_pos = self.map_to_image_space(pos)
        return 0 <= img_pos.x() < image_width and 0 <= img_pos.y() < image_height


if __name__ == "__main__":
    from VisionSystem.VisionSystem import VisionSystem
    from GlueDispensingApplication.vision.VisionService import VisionServiceSingleton
    import threading
    from PyQt6.QtWidgets import QWidget, QHBoxLayout

    # visionSystem = VisionSystem()
    visionSystem = VisionServiceSingleton.get_instance()

    def runCameraFeed():
        while True:
            visionSystem.run()

    threading.Thread(target=runCameraFeed, daemon=True).start()

    app = QApplication(sys.argv)

    # Main container widget
    main_window = QWidget()
    main_layout = QHBoxLayout(main_window)
    main_layout.setContentsMargins(0, 0, 0, 0)

    # Bezier editor on the left
    # contour = np.array([[[100, 100]], [[200, 100]], [[200, 200]], [[100, 200]]], dtype=np.int32)

    contourEditor = ContourEditor(visionSystem, image_path="imageDebug.png")
    main_layout.addWidget(contourEditor, stretch=4)

    # CreateWorkpieceForm on the right
    from pl_gui.PointManagerWidget import PointManagerWidget  # Replace with your actual import

    pointManagerWidget = PointManagerWidget(contourEditor)
    pointManagerWidget.setFixedWidth(350)  # Adjust sidebar width as needed
    main_layout.addWidget(pointManagerWidget, stretch=1)

    main_window.setGeometry(100, 100, 1600, 800)
    main_window.setWindowTitle("Bezier Editor with Sidebar")
    main_window.show()

    sys.exit(app.exec())
