import matplotlib.pyplot as plt

# Define the list of points
points = [(0.6, 0.2), (0.7, 0.35), (0.5, 0.1), (0.9, 0.05), (1, 0)]

# Separate x and y coordinates into two separate lists
x_coords = [point[0] for point in points]
y_coords = [point[1] for point in points]

# Create a plot with the x and y coordinates
plt.plot(x_coords, y_coords)

# Add labels to the axes and a title to the plot
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Connecting Points')

# Show the plot
plt.show()
