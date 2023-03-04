import numpy as np
import matplotlib.pyplot as plt
import mpltern


def generate_points_on_triangle(num_points):
    # Generate equally spaced barycentric coordinates in a unit square
    nb_points = int((num_points+1)*(num_points+2)/2)
    bary_coords = np.zeros((nb_points, 3))
    k = 0
    for i in range(num_points+1):
        for j in range(num_points+1):
            print(i, j)
            x, y = float(i) / num_points, float(j) / num_points
            z = 1.0 - x - y
            print(x, y, z)
            if z >= -1e-10:
                bary_coords[k] = np.array([x, y, z])
                k += 1
                if k == nb_points:
                    print(k)
                    break
        if k == nb_points:
            break

    print(bary_coords)

    return bary_coords

def replicator_dynamics(vec, payoff):
    x, y, z = vec[0], vec[1], vec[2]
    x_dot = x * (payoff.dot(vec)[0] - vec.dot(payoff.dot(vec)))
    y_dot = y * (payoff.dot(vec)[1] - vec.dot(payoff.dot(vec)))
    z_dot = z * (payoff.dot(vec)[2] - vec.dot(payoff.dot(vec)))

    return np.array([x_dot, y_dot, z_dot])

ax = plt.subplot(projection='ternary')

points = generate_points_on_triangle(20)

payoff_matrixA = np.array([[0, -0.25, 0.5], [0.25, 0, -0.05], [-0.5, 0.05, 0]])
# payoff_matrixA = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])

ds = []
for point in points:
    ds.append(replicator_dynamics(point, payoff_matrixA))
ds = np.array(ds)

print(ds)

ax.quiver(points[:, 0], points[:, 1], points[:, 2], ds[:, 0], ds[:, 1], ds[:, 2])
plt.show()

