import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtCore import QPointF
import cv2


def contour_to_bezier(contour, control_point_ratio=0.5):
    """
    Converts an OpenCV contour into a list of Bezier segments.

    Args:
        contour (list of tuple or numpy array): A list of points representing the contour.
        control_point_ratio (float): Controls how far along the segment the control points will be.
                                      Higher values make the control points closer to the segment.

    Returns:
        List of Bezier segments represented by start points, control points, and end points.
    """
    bezier_segments = []

    # Loop through the contour and create Bezier segments
    for i in range(len(contour)):
        # Unpack the points correctly
        start_point = contour[i][0]  # Each point is in a shape of (x, y)
        end_point = contour[(i + 1) % len(contour)][0]  # Wrap around to form a closed loop

        # Calculate control points (midpoints for simplicity, this can be refined)
        control_point_1 = QPointF(
            (start_point[0] + end_point[0]) * control_point_ratio,
            (start_point[1] + end_point[1]) * control_point_ratio
        )

        control_point_2 = QPointF(
            (start_point[0] + end_point[0]) * (1 - control_point_ratio),
            (start_point[1] + end_point[1]) * (1 - control_point_ratio)
        )

        # Store the segment (points and controls)
        bezier_segments.append({
            'points': [QPointF(start_point[0], start_point[1]), QPointF(end_point[0], end_point[1])],
            'controls': [control_point_1, control_point_2]
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


# Example usage:
# OpenCV contour obtained from cv2.findContours() (as a numpy array of points)
contour = np.array([[[100, 100]], [[200, 100]], [[200, 200]], [[100, 200]]], dtype=np.int32)

# Convert contour to Bezier
bezier_segments = contour_to_bezier(contour)

# Plot the contour and Bezier curves
plot_contour_and_bezier(contour, bezier_segments)
