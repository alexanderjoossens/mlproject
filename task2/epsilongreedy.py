import matplotlib.pyplot as plt
import numpy as np
import random
import pyspiel
from open_spiel.python.egt.utils import game_payoffs_array
from open_spiel.python.egt import visualization
from matplotlib.figure import Figure
from matplotlib.quiver import Quiver

# Create the figure and the Axes object
fig = plt.figure()
ax = fig.add_subplot()


epsilon =  0.5

payoffA = np.array([[-1, 1], [1, -1]])
payoffB = np.array([[1, -1], [-1, 1]])

payoffA = np.array([[3, 0], [0, 2]])
payoffB = np.array([[2, 0], [0, 3]])

# payoffA = np.array([[-1, -4], [0, -3]])
# payoffB = np.array([[-1, -4], [0, -3]])

# payoffA = np.array([[-1, 1], [1, -1]])
# payoffB = np.array([[-1, 1], [1, -1]])

game = pyspiel.create_matrix_game(payoffA, payoffB)
payoff_tensor = game_payoffs_array(game)

rewardsP1  = [0, 0]
countsP1   = [0, 0]
averagerewardsP1 = [0, 0]

rewardsP2  = [0, 0]
countsP2   = [0, 0]
averagerewardsP2 = [0, 0]

P1_action1_freqs = []
P2_action1_freqs = []

episodes = 10000

for i in range(episodes):
    eps = epsilon**(i/100)
    if (random.random() < eps):
        p1 = random.randint(0, 1) # explore
    else:
        p1 = np.argmax(averagerewardsP1) # exploit
    
    if (random.random() < eps):
        p2 = random.randint(0, 1)
    else:
        p2 = np.argmax(averagerewardsP2)
    
    rewardP1 = payoff_tensor[0][p1][p2]
    rewardP2 = payoff_tensor[1][p1][p2]

    rewardsP1[p1] += rewardP1
    rewardsP2[p2] += rewardP2
    countsP1[p1] += 1
    countsP2[p2] += 1
    averagerewardsP1[p1] = rewardsP1[p1] / countsP1[p1]
    averagerewardsP2[p2] = rewardsP2[p2] / countsP2[p2]

    if i % 10 == 0:
        freq1 = countsP1[1] / np.sum(countsP1)
        freq2 = countsP2[1] / np.sum(countsP2)
        if i != 0 and abs(freq1 - P1_action1_freqs[-1]) < 1e-4 and abs(freq2 - P2_action1_freqs[-1]) < 1e-4:
            print(freq1, freq2)
            break
        else:
            P1_action1_freqs.append(countsP1[1] / np.sum(countsP1))
            P2_action1_freqs.append(countsP2[1] / np.sum(countsP2))

# Define replicator dynamics
def replicator_dynamics(X, Y):
    x_dot = np.zeros_like(X)
    y_dot = np.zeros_like(Y)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            x = X[i, j]
            y = Y[i, j]
            x_vec = np.array([x, 1-x])
            y_vec = np.array([y, 1-y])
            x_dot[i, j] = x * (payoffA.dot(y_vec)[0] - x_vec.dot(payoffA.dot(y_vec)))
            y_dot[i, j] = y * (payoffB.dot(x_vec)[0] - y_vec.dot(payoffB.dot(x_vec)))

    return x_dot, y_dot

# Define the grid of initial conditions
x = np.linspace(0, 1, 20)
y = np.linspace(0, 1, 20)
X, Y = np.meshgrid(x, y)

# Compute the direction vectors
U, V = replicator_dynamics(X, Y)

# Plot the directional field
ax.quiver(X, Y, U, V)

# Set the plot limits and labels
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel('Probability of Player 1 picking Opera')
ax.set_ylabel('Probability of Player 2 picking Opera')

# Show the plot
# plt.streamplot(X, Y, U, V)

print(P1_action1_freqs)
print(P2_action1_freqs)

plt.plot(P1_action1_freqs, P2_action1_freqs)
plt.show()



    