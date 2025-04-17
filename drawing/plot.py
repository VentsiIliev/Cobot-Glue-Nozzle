import matplotlib.pyplot as plt
import numpy as np

# Contour data
contour1 = np.array([[[[0.0, 0.0]], [[134.0, 0.0]]],
                     [[[134.0, 0.0]], [[134.0, 58.5]]],
                     [[[134.0, 58.5]], [[0.0, 58.5]]],
                     [[[0.0, 58.5]], [[0.0, 0.0]]]])

contour2 = np.array([[[-59.730717, 590.1483]],
                     [[-72.00659, 541.79987]],
                     [[51.56464, 510.34686]],
                     [[63.199547, 560.048]],
                     [[-56.837833, 590.9858]],
                     [[-59.730717, 590.1483]]])

# Extract points for Contour1
contour1_points = []
for segment in contour1:
    for point in segment:
        contour1_points.append(point[0])
contour1_points = np.array(contour1_points)

# Extract points for Contour2
contour2_points = contour2[:, 0, :]

# Plotting
plt.figure(figsize=(8, 6))

# Plot Contour1
plt.plot(contour1_points[:, 0], contour1_points[:, 1], label="Contour1", color="blue", marker="o")

# Plot Contour2
plt.plot(contour2_points[:, 0], contour2_points[:, 1], label="Contour2", color="red", marker="o")

# Formatting
plt.title("Contours Plot")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)
plt.axis("equal")

# Show plot
plt.show()