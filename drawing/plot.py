import matplotlib.pyplot as plt
import numpy as np

# Points data
points = [
    [
        [117.0, 138.5]
    ],
    [
        [247.0, 138.5]
    ],
    [
        [247.0, 203.5]
    ],
    [
        [117.0, 203.5]
    ]
]

# Convert to NumPy array for easier manipulation
points = np.array(points).reshape(-1, 2)

# Extract x and y coordinates
x = points[:, 0]
y = points[:, 1]

# Plot the points
plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o', color='blue', label="Points")
plt.fill(x, y, color='lightblue', alpha=0.3)  # Optional: Fill the shape

# Add labels, legend, and grid
plt.title("Points Plot")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()