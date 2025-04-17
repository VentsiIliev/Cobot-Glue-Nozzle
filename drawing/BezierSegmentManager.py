from PyQt6.QtCore import QPointF

class BezierSegmentManager:
    def __init__(self):
        self.segments = [{'points': [], 'controls': []}]

    def add_point(self, pos):
        current = self.segments[-1]
        current['points'].append(pos)
        if len(current['points']) >= 2:
            mid = (current['points'][-2] + current['points'][-1]) / 2
            current['controls'].append(mid)

    def remove_control_point_at(self, pos, threshold=10):
        for seg in self.segments:
            for i, pt in enumerate(seg['controls']):
                if (pt - pos).manhattanLength() < threshold:
                    del seg['controls'][i]
                    if i + 1 < len(seg['points']):
                        del seg['points'][i + 1]
                    return True
        return False

    def find_drag_target(self, pos, threshold=10):
        for seg_index, seg in enumerate(self.segments):
            for i, pt in enumerate(seg['controls']):
                if (pt - pos).manhattanLength() < threshold:
                    return 'control', seg_index, i
            for i, pt in enumerate(seg['points']):
                if (pt - pos).manhattanLength() < threshold:
                    return 'anchor', seg_index, i
        return None

    def start_new_segment(self):
        self.segments.append({'points': [], 'controls': []})

    def move_point(self, role, seg_index, idx, new_pos):
        segment = self.segments[seg_index]
        points = segment['points']
        controls = segment['controls']

        if role == 'anchor':
            old_pos = points[idx]
            delta = new_pos - old_pos
            points[idx] = new_pos

            if idx > 0 and idx - 1 < len(controls):
                p0 = points[idx - 1]
                ctrl = controls[idx - 1]
                if self.is_on_line(p0, ctrl, old_pos):
                    controls[idx - 1] = (p0 + new_pos) / 2

            if idx < len(points) - 1 and idx < len(controls):
                p1 = points[idx + 1]
                ctrl = controls[idx]
                if self.is_on_line(old_pos, ctrl, p1):
                    controls[idx] = (new_pos + p1) / 2

        elif role == 'control':
            controls[idx] = new_pos

    @staticmethod
    def is_on_line(p0, cp, p1, threshold=1.0):
        dx = p1.x() - p0.x()
        dy = p1.y() - p0.y()
        if dx == dy == 0:
            return False
        distance = abs(dy * cp.x() - dx * cp.y() + p1.x() * p0.y() - p1.y() * p0.x()) / ((dx ** 2 + dy ** 2) ** 0.5)
        return distance < threshold

    def get_segments(self):
        return self.segments

    def get_robot_path(self, samples_per_segment=5):
        path_points = []

        def is_cp_effective(p0, cp, p1, threshold=1.0):
            dx = p1.x() - p0.x()
            dy = p1.y() - p0.y()
            if dx == dy == 0:
                return False
            distance = abs(dy * cp.x() - dx * cp.y() + p1.x() * p0.y() - p1.y() * p0.x()) / ((dx ** 2 + dy ** 2) ** 0.5)
            return distance > threshold

        for segment in self.segments:
            points, controls = segment['points'], segment['controls']
            for i in range(1, len(points)):
                p0, p1 = points[i - 1], points[i]
                if i - 1 < len(controls) and is_cp_effective(p0, controls[i - 1], p1):
                    for t in [j / samples_per_segment for j in range(samples_per_segment + 1)]:
                        x = (1 - t) ** 2 * p0.x() + 2 * (1 - t) * t * controls[i - 1].x() + t ** 2 * p1.x()
                        y = (1 - t) ** 2 * p0.y() + 2 * (1 - t) * t * controls[i - 1].y() + t ** 2 * p1.y()
                        path_points.append(QPointF(x, y))
                else:
                    path_points.extend([p0, p1])
        return path_points

    def reset_control_point(self, seg_index, ctrl_idx):
        segment = self.segments[seg_index]
        points = segment['points']
        controls = segment['controls']
        if ctrl_idx + 1 < len(points):
            controls[ctrl_idx] = (points[ctrl_idx] + points[ctrl_idx + 1]) / 2

    def remove_point(self, role, seg_index, idx):
        if seg_index >= len(self.segments):
            raise IndexError("Segment index out of range")

        segment = self.segments[seg_index]
        if role == 'anchor':
            if idx >= len(segment['points']):
                raise IndexError("Anchor index out of range")
            del segment['points'][idx]
        elif role == 'control':
            if idx >= len(segment['controls']):
                raise IndexError("Control index out of range")
            del segment['controls'][idx]
        else:
            raise ValueError("Role must be 'anchor' or 'control'")

    def remove_specific_point(self, role, seg_index, idx):
        try:
            segment = self.segments[seg_index]
            if role == 'anchor' and idx < len(segment['points']):
                segment['points'].pop(idx)
                return True
            elif role == 'control' and idx < len(segment['controls']):
                segment['controls'].pop(idx)
                return True
        except Exception as e:
            print(f"Error removing specific point: {e}")
        return False

    def insert_midpoint(self, seg_index, ctrl_index, pt):
        try:
            # Get the segment by index
            segment = self.segments[seg_index]
            points = segment['points']
            controls = segment['controls']

            # Ensure we have a valid control index
            if ctrl_index >= len(controls):
                raise ValueError("Control index out of range.")

            # Assuming you are working with a quadratic Bezier curve between points
            p0 = points[ctrl_index]
            p1 = controls[ctrl_index]
            p2 = points[ctrl_index + 1] if ctrl_index + 1 < len(points) else controls[ctrl_index]

            # Calculate the midpoint for quadratic or cubic Bezier
            mid_point = self.evaluate_quadratic_bezier(p0, p1, p2, 0.5)

            # Insert the midpoint as a new control point or adjust accordingly
            controls.insert(ctrl_index + 1, mid_point)  # Insert midpoint as a control point
            points.insert(ctrl_index + 1, mid_point)  # Optionally, insert as an anchor point

            # Update the segment with the new control and points list
            segment['points'] = points
            segment['controls'] = controls

            print(f"Midpoint inserted at index {ctrl_index + 1}: {mid_point}")

        except Exception as e:
            print(f"Error inserting midpoint: {e}")

    def evaluate_quadratic_bezier(self, p0, p1, p2, t):
        # Simple quadratic Bezier curve evaluation: (1 - t)^2 * p0 + 2(1 - t) * t * p1 + t^2 * p2
        return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2