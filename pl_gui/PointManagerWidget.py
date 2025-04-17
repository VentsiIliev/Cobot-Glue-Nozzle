from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from PyQt6.QtCore import Qt


class PointManagerWidget(QWidget):
    def __init__(self, contour_editor=None):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.setStyleSheet("background-color: #f5f5f5;")
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.contour_editor = contour_editor
        if self.contour_editor:
            self.contour_editor.pointsUpdated.connect(self.refresh_points)

        self.point_list = QListWidget()
        self.point_list.currentItemChanged.connect(self.highlight_selected_point)
        self.layout().addWidget(self.point_list)

        self.refresh_button = QPushButton("Refresh Points")
        self.refresh_button.clicked.connect(self.refresh_points)
        self.layout().addWidget(self.refresh_button)

        self.remove_button = QPushButton("Remove Selected Point")
        self.remove_button.clicked.connect(self.remove_selected_point)
        self.layout().addWidget(self.remove_button)


        # Add the toggle pinch gesture button
        self.toggle_pinch_button = QPushButton("Enable Pinch Gesture")
        self.toggle_pinch_button.clicked.connect(self.toggle_pinch_gesture)
        self.layout().addWidget(self.toggle_pinch_button)

    def toggle_pinch_gesture(self):
        if not self.contour_editor:
            QMessageBox.warning(self, "Error", "Contour editor is not set.")
            return

        # Call the toggle_zooming method
        self.contour_editor.toggle_zooming()

        # Update button text based on the new state
        if self.contour_editor.is_zooming:
            self.toggle_pinch_button.setText("Disable Zooming")
        else:
            self.toggle_pinch_button.setText("Enable Zooming")

    def setContourEditor(self, editor):
        self.contour_editor = editor

    def refresh_points(self):
        self.point_list.clear()
        if not self.contour_editor:
            return
        segments = self.contour_editor.manager.get_segments()
        for seg_index, segment in enumerate(segments):
            for i, pt in enumerate(segment['points']):
                self.point_list.addItem(f"SEG {seg_index} | P{i}: ({pt.x():.1f}, {pt.y():.1f})")
            for i, ctrl in enumerate(segment['controls']):
                self.point_list.addItem(f"SEG {seg_index} | C{i}: ({ctrl.x():.1f}, {ctrl.y():.1f})")

    def highlight_selected_point(self):
        item = self.point_list.currentItem()
        if not item or not self.contour_editor:
            return

        text = item.text()
        try:
            seg_index = int(text.split('|')[0].split()[1])
            role_info = text.split('|')[1].strip()
            if role_info.startswith('P'):
                idx = int(role_info[1:].split(':')[0])
                self.contour_editor.selected_point_info = ('anchor', seg_index, idx)
            elif role_info.startswith('C'):
                idx = int(role_info[1:].split(':')[0])
                self.contour_editor.selected_point_info = ('control', seg_index, idx)
            self.contour_editor.update()
        except Exception as e:
            print(f"Selection error: {e}")

    def remove_selected_point(self):
        selected_item = self.point_list.currentItem()
        if not selected_item or not self.contour_editor:
            return
        try:
            text = selected_item.text()
            seg_index = int(text.split('|')[0].split()[1])
            role_info = text.split('|')[1].strip()

            if role_info.startswith('P'):
                idx = int(role_info[1:].split(':')[0])
                self.contour_editor.manager.remove_point('anchor', seg_index, idx)
            elif role_info.startswith('C'):
                idx = int(role_info[1:].split(':')[0])
                self.contour_editor.manager.remove_point('control', seg_index, idx)

            self.refresh_points()
            self.contour_editor.update()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def insert_midpoint(self):
        if not self.contour_editor:
            return

        selected_item = self.point_list.currentItem()
        if not selected_item:
            QMessageBox.information(self, "Insert Point",
                                    "Please select a segment control or anchor to insert midpoint.")
            return

        text = selected_item.text()
        try:
            seg_index = int(text.split('|')[0].split()[1])
            role_info = text.split('|')[1].strip()

            if role_info.startswith('P'):
                idx = int(role_info[1:].split(':')[0])
                points = self.contour_editor.manager.segments[seg_index]['points']
                controls = self.contour_editor.manager.segments[seg_index]['controls']

                if idx < len(points) - 1:
                    p0 = points[idx]
                    p1 = points[idx + 1]
                    ctrl = controls[idx] if idx < len(controls) else (p0 + p1) / 2
                    mid = self.contour_editor.manager.evaluate_quadratic_bezier(p0, ctrl, p1, 0.5)

                    # Insert point
                    new_ctrl1 = (p0 + mid) / 2
                    new_ctrl2 = (mid + p1) / 2
                    points.insert(idx + 1, mid)
                    controls[idx] = new_ctrl1
                    controls.insert(idx + 1, new_ctrl2)

                    self.refresh_points()
                    self.contour_editor.update()
                    self.contour_editor.pointsUpdated.emit()
                else:
                    QMessageBox.warning(self, "Insert Point", "Cannot insert after the last anchor.")
            else:
                QMessageBox.warning(self, "Insert Point", "Please select an anchor (P) to insert after.")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

