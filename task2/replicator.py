import numpy as np
import matplotlib.pyplot as plt


# Create the figure and the Axes object
fig = plt.figure()
ax = fig.add_subplot()

# Define the payoff matrix
payoff_matrixA = np.array([[-1, 1], [1, -1]])
payoff_matrixB = np.array([[-1, -4], [0, -3]])

# Define the replicator dynamics function
def replicator_dynamics(X, Y):
    x_dot = np.zeros_like(X)
    y_dot = np.zeros_like(Y)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            x = X[i, j]
            y = Y[i, j]
            x_vec = np.array([x, 1-x])
            y_vec = np.array([y, 1-y])
            x_dot[i, j] = x * (payoff_matrixA.dot(y_vec)[0] - x_vec.dot(payoff_matrixA.dot(y_vec)))
            y_dot[i, j] = y * (payoff_matrixA.dot(x_vec)[0] - y_vec.dot(payoff_matrixA.dot(x_vec)))

    return x_dot, y_dot


# Define the grid of initial conditions
x = np.linspace(0, 1, 20)
y = np.linspace(0, 1, 20)
X, Y = np.meshgrid(x, y)

# Compute the direction vectors
U, V = replicator_dynamics(X, Y)

# Plot the directional field
#ax.quiver(X, Y, U, V)

# Set the plot limits and labels
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel('Probability of Player 1 picking Opera')
ax.set_ylabel('Probability of Player 2 picking Opera')

# Show the plot
plt.streamplot(X, Y, U, V)

plt.show()
