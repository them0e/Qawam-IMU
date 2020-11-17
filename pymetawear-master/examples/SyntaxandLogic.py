"""
============
Euler Angles
============

Any rotation can be represented by three consecutive rotations about three
basis vectors. Here we use either the x-y-z convention or the z-y-x convention.
"""
print(__doc__)

import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pytransform3d.rotations import *

with open('EU.csv', newline='') as csvfile:
    EU = list(csv.reader(csvfile))
EU = np.array(EU)
x = EU[0:]
x = x[0]
y = EU[1:]
y = y[0]
z = EU[2:]
z = z[0]

for i in range(len(x)):
    plot_basis(x[i], y[i], z[i])

#
# ax = plot_basis(R=np.eye(3), ax_s=2)
# alpha, beta, gamma = np.pi, np.pi, np.pi
#
# p = np.array([0.6, 0.4, 0.4])
# R = matrix_from_euler_xyz([alpha, 0, 0])
# plot_basis(ax, R, p)
# R = matrix_from_euler_xyz([alpha, beta, 0])
# plot_basis(ax, R, 2 * p)
# R = matrix_from_euler_xyz([alpha, beta, gamma])
# plot_basis(ax, R, 3 * p)
#
# p = np.array([0.4, 0.6, 0.4])
# R = matrix_from_euler_zyx([alpha, 0, 0])
# plot_basis(ax, R, p, alpha=0.5)
# R = matrix_from_euler_zyx([alpha, beta, 0])
# plot_basis(ax, R, 2 * p, alpha=0.5)
# R = matrix_from_euler_zyx([alpha, beta, gamma])
# plot_basis(ax, R, 3 * p, alpha=0.5)

plt.show()