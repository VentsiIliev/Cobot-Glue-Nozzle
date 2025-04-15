from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QImage, QPen, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QPointF
import sys
import matplotlib.pyplot as plt

# from drawing.testTransformPoints import visionSystem


class BezierEditor(QWidget):
    def __init__(self,visionSystem, image_path=None):
        super().__init__()
        self.setWindowTitle("Editable Bezier Curves")
        self.setGeometry(100, 100, 1280, 720)
        self.visionSystem = visionSystem
        # self.points = []  # Main points (anchors)
        # self.control_points = []  # Control points for curves
        self.segments = []  # Each segment is a dict: {'points': [], 'controls': []}
        self.segments.append({'points': [], 'controls': []})

        self.dragging_point = None
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self.setAutoFillBackground(False)



        # Load image if path is provided
        if image_path:
            self.image = QImage(image_path)
        else:
            self.image = QImage(1280, 720, QImage.Format.Format_RGB32)  # Fallback if no image is passed
            self.image.fill(Qt.white)  # Fill the image with a white background


    def update_image(self, image_input):
        """Update the image displayed in the editor. Accepts path or QImage."""
        if isinstance(image_input, str):
            new_image = QImage(image_input)
            if new_image.isNull():
                print(f"Failed to load image from path: {image_input}")
                return
            self.image = new_image
        elif isinstance(image_input, QImage):
            self.image = image_input
        else:
            print("Unsupported image input type.")
            return

        self.update()  # Repaint the widget

    def mousePressEvent(self, event):
        pos = event.position()

        if event.button() == Qt.MouseButton.RightButton:
            # Check for control point deletion across all segments
            for seg in self.segments:
                for i, pt in enumerate(seg['controls']):
                    if (pt - pos).manhattanLength() < 10:
                        print(f"Deleting control point {i}")
                        del seg['controls'][i]
                        if i + 1 < len(seg['points']):
                            del seg['points'][i + 1]
                        self.update()
                        return

        elif event.button() == Qt.MouseButton.LeftButton:
            current = self.segments[-1]

            for i, pt in enumerate(current['controls']):
                if (pt - pos).manhattanLength() < 10:
                    self.dragging_point = ('control', len(self.segments) - 1, i)
                    return
            for i, pt in enumerate(current['points']):
                if (pt - pos).manhattanLength() < 10:
                    self.dragging_point = ('anchor', len(self.segments) - 1, i)
                    return

            current['points'].append(pos)
            if len(current['points']) >= 2:
                mid = (current['points'][-2] + current['points'][-1]) / 2
                current['controls'].append(mid)
            self.update()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom_factor *= self.zoom_step
        else:
            self.zoom_factor /= self.zoom_step
        self.update()

    def mouseMoveEvent(self, event):
        if self.dragging_point is not None:
            role, seg_index, index = self.dragging_point
            segment = self.segments[seg_index]

            if role == 'anchor':
                segment['points'][index] = event.position()
            elif role == 'control':
                segment['controls'][index] = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragging_point = None

    def paintEvent(self, event):
        painter = QPainter(self)
        try:
            if not painter.isActive():
                print("Painter is not active!")
                return

            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.drawImage(0, 0, self.image)

            for segment in self.segments:
                points = segment['points']
                controls = segment['controls']

                if len(points) >= 2:
                    pen = QPen(Qt.GlobalColor.black, 2)
                    painter.setPen(pen)
                    painter.setBrush(Qt.BrushStyle.NoBrush)  # Not filling
                    path = QPainterPath()
                    path.moveTo(points[0])

                    for i in range(1, len(points)):
                        if i - 1 < len(controls):
                            cp = controls[i - 1]
                            path.quadTo(cp, points[i])
                    painter.drawPath(path)

                # Draw anchors
                painter.setPen(QPen(Qt.PenStyle.NoPen))  # <-- Correct NoPen usage
                brush = QBrush(Qt.GlobalColor.blue)
                for pt in points:
                    painter.setBrush(brush)
                    painter.drawEllipse(pt, 5, 5)

                # Draw control points
                brush = QBrush(Qt.GlobalColor.red)
                for pt in controls:
                    painter.setBrush(brush)
                    painter.drawEllipse(pt, 5, 5)

                # Draw helper lines
                pen = QPen(Qt.GlobalColor.gray, 1, Qt.PenStyle.DashLine)
                painter.setPen(pen)
                for i in range(1, len(points)):
                    if i - 1 < len(controls):
                        painter.drawLine(points[i - 1], controls[i - 1])
                        painter.drawLine(controls[i - 1], points[i])

        finally:
            painter.end()  # Always safely close the painter

    def get_robot_path(self, samples_per_segment=5):
        path_points = []

        def is_control_point_effective(p0, cp, p1, threshold=1.0):
            dx = p1.x() - p0.x()
            dy = p1.y() - p0.y()
            if dx == dy == 0:
                return False
            numerator = abs(dy * cp.x() - dx * cp.y() + p1.x() * p0.y() - p1.y() * p0.x())
            denominator = (dx ** 2 + dy ** 2) ** 0.5
            distance = numerator / denominator
            return distance > threshold

        for segment in self.segments:
            points = segment['points']
            controls = segment['controls']

            for i in range(1, len(points)):
                p0 = points[i - 1]
                p1 = points[i]

                if i - 1 < len(controls):
                    cp = controls[i - 1]
                    if is_control_point_effective(p0, cp, p1):
                        for t in [j / samples_per_segment for j in range(samples_per_segment + 1)]:
                            x = (1 - t) ** 2 * p0.x() + 2 * (1 - t) * t * cp.x() + t ** 2 * p1.x()
                            y = (1 - t) ** 2 * p0.y() + 2 * (1 - t) * t * cp.y() + t ** 2 * p1.y()
                            path_points.append(QPointF(x, y))
                    else:
                        path_points.extend([p0, p1])
                else:
                    path_points.extend([p0, p1])

        return path_points

    def save_robot_path_to_txt(self, filename="robot_path.txt", samples_per_segment=5):
        path = self.get_robot_path(samples_per_segment)
        try:
            with open(filename, 'w') as f:
                for point in path:
                    f.write(f"{point.x():.3f}, {point.y():.3f}\n")
            print(f"Saved robot path to {filename} with {len(path)} points.")
        except Exception as e:
            print(f"Error saving robot path: {e}")

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_N:
            print("Starting a new segment")
            self.segments.append({'points': [], 'controls': []})
            self.update()

        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.save_robot_path_to_txt("robot_path.txt", samples_per_segment=5)
            self.plot_robot_path()
            import testTransformPoints
            print("Robot path saved to 'robot_path.txt'")

        if event.key() == Qt.Key.Key_Space:
            print("Spacebar pressed, updating image.")
            # Capture an image using the VisionSystem
            image = self.visionSystem.captureImage()  # Returns a numpy.ndarray
            if image is None:
                print("Failed to capture image.")
                return

            # Convert numpy.ndarray to QImage
            height, width, channels = image.shape
            bytes_per_line = channels * width
            if channels == 3:  # RGB
                qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            elif channels == 4:  # RGBA
                qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format.Format_RGBA888)
            else:
                print("Unsupported image format.")
                return

            self.update_image(qimage)  # Update the image displayed

    def plot_robot_path(self, filename="robot_path.txt"):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            if not lines:
                print("No data in path file.")
                return

            x_vals = []
            y_vals = []
            for line in lines:
                try:
                    x_str, y_str = line.strip().split(',')
                    x_vals.append(float(x_str))
                    y_vals.append(float(y_str))
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")

            plt.figure(figsize=(12.8, 7.2))  # Maintain aspect ratio of 1280x720
            plt.plot(x_vals, y_vals, 'b-', label="Robot Path")

            # Optional: also show anchor and control points if available
            if self.points:
                plt.scatter([p.x() for p in self.points], [p.y() for p in self.points], color='blue',
                            label="Anchor Points")
            if self.control_points:
                plt.scatter([p.x() for p in self.control_points], [p.y() for p in self.control_points], color='red',
                            label="Control Points")

            # Fix Y-axis and adjust limits
            # Invert the Y-axis so it matches the PyQt coordinate system
            plt.gca().invert_yaxis()  # Invert Y-axis to match PyQt's coordinate system
            plt.xlim(0, self.width())  # Set X-axis range to widget width (1280)
            plt.ylim(self.height(), 0)  # Set Y-axis range to widget height (720), invert to match PyQt

            # Set the plot title and labels
            plt.title("Robot Path Visualization")
            plt.xlabel("X")
            plt.ylabel("Y")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            plt.show()

        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error reading path from file: {e}")


if __name__ == "__main__":
    from VisionSystem.VisionSystem import VisionSystem
    import threading

    visionSystem = VisionSystem()

    def runCameraFeed():
        while True:
            visionSystem.run()


    cameraThread = threading.Thread(target=runCameraFeed, daemon=True)
    cameraThread.start()

    app = QApplication(sys.argv)
    window = BezierEditor(visionSystem,image_path="imageDebug.png")  # Replace with actual image path
    window.show()

    sys.exit(app.exec())
