import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtCore import QPointF
import cv2


def contour_to_bezier(contour, control_point_ratio=0.5):
    """
    Converts an OpenCV contour into a list of quadratic Bezier segments.

    Args:
        contour (list or numpy array): OpenCV-style contour where each point is [[x, y]].
        control_point_ratio (float): Position along the line between start and end for control point.

    Returns:
        List of dicts with keys: 'points' (2 anchor points) and 'controls' (1 control point).
    """
    bezier_segments = []

    for i in range(len(contour)):
        start = contour[i][0]
        end = contour[(i + 1) % len(contour)][0]  # Wrap around

        start_pt = QPointF(start[0], start[1])
        end_pt = QPointF(end[0], end[1])

        # Midpoint (you can tweak this for smoothing/shaping)
        control_x = (1 - control_point_ratio) * start[0] + control_point_ratio * end[0]
        control_y = (1 - control_point_ratio) * start[1] + control_point_ratio * end[1]
        control_pt = QPointF(control_x, control_y)

        bezier_segments.append({
            'points': [start_pt, end_pt],
            'controls': [control_pt]
        })

    return bezier_segments


def plot_contour_and_bezier(contour, bezier_segments):
    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Plot the original contour as a polygon (connect the points)
    contour_points = np.array([point[0] for point in contour], dtype=np.int32)
    plt.plot(contour_points[:, 0], contour_points[:, 1], label="Contour", color="blue", marker="o")

    # Plot the Bezier curves
    for segment in bezier_segments:
        points = segment['points']
        controls = segment['controls']
        # For each segment, plot the bezier curve using control points
        bezier_points = []
        for t in np.linspace(0, 1, 100):  # t from 0 to 1 with 100 samples
            x = (1 - t) ** 2 * points[0].x() + 2 * (1 - t) * t * controls[0].x() + t ** 2 * points[1].x()
            y = (1 - t) ** 2 * points[0].y() + 2 * (1 - t) * t * controls[0].y() + t ** 2 * points[1].y()
            bezier_points.append([x, y])

        bezier_points = np.array(bezier_points)
        plt.plot(bezier_points[:, 0], bezier_points[:, 1], label="Bezier Curve", color="red")

    # Add labels and legend
    plt.title("Contour and Bezier Curves")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.gca().invert_yaxis()  # To match typical image coordinates
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# # Example usage:
# # OpenCV contour obtained from cv2.findContours() (as a numpy array of points)
# contour = np.array([[[100, 100]], [[200, 100]], [[200, 200]], [[100, 200]]], dtype=np.int32)
#
# # Convert contour to Bezier
# bezier_segments = contour_to_bezier(contour)
#
# # Plot the contour and Bezier curves
# plot_contour_and_bezier(contour, bezier_segments)
