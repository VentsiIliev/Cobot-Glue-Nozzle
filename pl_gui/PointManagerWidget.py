from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox, QTreeWidget, QTreeWidgetItem
)
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

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Point Type", "Coordinates", "Current"])
        self.tree.itemClicked.connect(self.highlight_selected_point)
        self.tree.itemChanged.connect(self.handle_segment_toggle)
        self.layout().addWidget(self.tree)

        self.refresh_button = QPushButton("Refresh Points")
        self.refresh_button.clicked.connect(self.refresh_points)
        self.layout().addWidget(self.refresh_button)

        self.remove_button = QPushButton("Remove Selected Point")
        self.remove_button.clicked.connect(self.remove_selected_point)
        self.layout().addWidget(self.remove_button)

        self.toggle_pinch_button = QPushButton("Enable Pinch Gesture")
        self.toggle_pinch_button.clicked.connect(self.toggle_pinch_gesture)
        self.layout().addWidget(self.toggle_pinch_button)

    def toggle_pinch_gesture(self):
        if not self.contour_editor:
            QMessageBox.warning(self, "Error", "Contour editor is not set.")
            return

        self.contour_editor.toggle_zooming()
        self.toggle_pinch_button.setText(
            "Disable Zooming" if self.contour_editor.is_zooming else "Enable Zooming"
        )

    def refresh_points(self):
        self.tree.blockSignals(True)
        self.tree.clear()
        if not self.contour_editor:
            self.tree.blockSignals(False)
            return

        segments = self.contour_editor.manager.get_segments()
        for seg_index, segment in enumerate(segments):
            seg_item = QTreeWidgetItem([f"Segment {seg_index}", "", ""])
            seg_item.setFlags(seg_item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable)

            # Visibility checkbox (column 0)
            seg_item.setCheckState(0,
                                   Qt.CheckState.Checked if segment.get('visible', True) else Qt.CheckState.Unchecked)

            # Current/active segment checkbox (column 2)
            is_active = self.contour_editor.manager.active_segment_index == seg_index
            current_state = Qt.CheckState.Checked if is_active else Qt.CheckState.Unchecked
            seg_item.setCheckState(2, current_state)

            seg_item.setExpanded(False)

            for i, pt in enumerate(segment['points']):
                child = QTreeWidgetItem(["P" + str(i), f"({pt.x():.1f}, {pt.y():.1f})", ""])
                seg_item.addChild(child)

            for i, ctrl in enumerate(segment['controls']):
                child = QTreeWidgetItem(["C" + str(i), f"({ctrl.x():.1f}, {ctrl.y():.1f})", ""])
                seg_item.addChild(child)

            self.tree.addTopLevelItem(seg_item)

        self.tree.blockSignals(False)

    def handle_segment_toggle(self, item, column):
        if not self.contour_editor or item.parent() is not None:
            return  # Only respond to top-level items

        seg_text = item.text(0)
        try:
            seg_index = int(seg_text.split()[-1])

            # Column 0: Visibility
            if column == 0:
                visible = item.checkState(0) == Qt.CheckState.Checked
                self.contour_editor.manager.set_segment_visibility(seg_index, visible)
                self.contour_editor.update()

            # Column 2: Current segment toggle
            elif column == 2:
                # Only one segment can be active at a time, so deactivate others
                if item.checkState(2) == Qt.CheckState.Checked:
                    # Deactivate all other segments
                    for i in range(self.tree.topLevelItemCount()):
                        other_item = self.tree.topLevelItem(i)
                        if other_item != item:
                            other_item.setCheckState(2, Qt.CheckState.Unchecked)

                    # Set the new active segment
                    self.contour_editor.manager.set_active_segment(seg_index)

                # Refresh to enforce only one active segment
                self.refresh_points()

        except Exception as e:
            print(f"Segment toggle error: {e}")

    def highlight_selected_point(self, item):
        if not item or not self.contour_editor:
            return

        parent = item.parent()
        if parent is None:
            return  # Skip segment headers (top-level items)

        # Determine the segment index
        seg_text = parent.text(0)
        try:
            seg_index = int(seg_text.split()[-1])

            # Handle point selection
            label = item.text(0)
            if label.startswith("P"):
                idx = int(label[1:])
                self.contour_editor.selected_point_info = ('anchor', seg_index, idx)
            elif label.startswith("C"):
                idx = int(label[1:])
                self.contour_editor.selected_point_info = ('control', seg_index, idx)

            self.contour_editor.update()
        except Exception as e:
            print(f"Selection error: {e}")

    def remove_selected_point(self):
        item = self.tree.currentItem()
        if not item or not self.contour_editor or not item.parent():
            return

        seg_text = item.parent().text(0)
        seg_index = int(seg_text.split()[-1])
        label = item.text(0)

        try:
            if label.startswith("P"):
                idx = int(label[1:])
                self.contour_editor.manager.remove_point('anchor', seg_index, idx)
            elif label.startswith("C"):
                idx = int(label[1:])
                self.contour_editor.manager.remove_point('control', seg_index, idx)

            self.refresh_points()
            self.contour_editor.update()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
