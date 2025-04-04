import cv2
import numpy as np

def zigZag( contour, spacing, direction):
    points = [tuple(point) for point in contour]
    zigzag_coords = []

    bbox = cv2.minAreaRect(np.array(points))
    box = cv2.boxPoints(bbox)
    center = np.mean(box, axis=0)  # More accurate center
    width, height = bbox[1]
    angle = bbox[2]

    if width < height:
        width, height = height, width
        angle += 90

    # Adjust for vertical direction
    if direction == "vertical":
        angle += 90

    # Generate zigzag points in rotated space
    direction = 1  # Start with positive direction
    for i in range(0, int(width), spacing):
        x_new = -width / 2 + i + center[0]  # Centered around bbox
        y_top = -height / 2 + center[1]
        y_bottom = height / 2 + center[1]

        if direction == 1:
            zigzag_coords.append((x_new, y_top))
            zigzag_coords.append((x_new, y_bottom))
        else:
            zigzag_coords.append((x_new, y_bottom))
            zigzag_coords.append((x_new, y_top))
        direction *= -1  # Alternate direction

    # Convert points to homogeneous coordinates for rotation
    points = np.array(zigzag_coords, dtype=np.float32)
    ones = np.ones((points.shape[0], 1))
    points_homogeneous = np.hstack([points, ones])

    # Compute rotation matrix
    theta = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta), center[0] - center[0] * np.cos(theta) + center[1] * np.sin(theta)],
        [np.sin(theta), np.cos(theta), center[1] - center[0] * np.sin(theta) - center[1] * np.cos(theta)],
        [0, 0, 1]
    ])

    # Apply rotation transformation
    rotated_points = (rotation_matrix @ points_homogeneous.T).T[:, :2].astype(int)

    return [(float(x), float(y)) for x, y in rotated_points]