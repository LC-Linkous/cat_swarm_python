#! /usr/bin/python3

##-------------------------------------------------------------------------------\
#   cat_swarm_quantum
#   '.src/himmelblau/graph.py'
#   generates graphs for function based on constraints and configurations
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: May 30, 2024
##-------------------------------------------------------------------------------\


import numpy as np
import matplotlib.pyplot as plt

import configs_F as f_c
# problem constraints - pulled from the function configs for the optimizers
LOWER_BOUNDS = f_c.LB[0]
UPPER_BOUNDS = f_c.UB[0]
LB_x = LOWER_BOUNDS[0] 
LB_y = LOWER_BOUNDS[1]
UB_x = UPPER_BOUNDS[0]
UB_y = UPPER_BOUNDS[1]
FUNC_F = f_c.OBJECTIVE_FUNC
GLOBAL_MIN = f_c.GLOBAL_MIN


#write out plot
plotname = "himmelblau_plots.png"


# Define range and step size
x = np.linspace(LB_x, UB_x, 600)
y = np.linspace(LB_y, UB_y, 600)
X, Y = np.meshgrid(x, y)

# Reshape X and Y to 1D arrays
X_flat = X.flatten()
Y_flat = Y.flatten()

# Stack X and Y to create coords as a 2D array
coords = np.stack((X_flat, Y_flat), axis=-1)

# Evaluate function

Z = []
for c in coords:
    z, noErr = FUNC_F(c)
    if noErr == True:
        Z.append(z)

# Convert Z to a NumPy array
Z = np.array(Z)

# Reshape Z to ensure it's 2-dimensional
Z = Z.reshape(X.shape)

# Create figure and subplots
fig = plt.figure(figsize=(14, 7))

# 3D projection subplot
ax1 = fig.add_subplot(121, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax1.set_xlabel('$x_1$')
ax1.set_ylabel('$x_2$')
ax1.set_zlabel('$f(x_1,x_2)$')
ax1.set_title('3D Projection')

# Contour plot subplot
ax2 = fig.add_subplot(122)
contour = ax2.contourf(X, Y, Z, cmap='viridis')
# Add white outline on contours
ax2.contour(X, Y, Z, colors='white', linewidths=0.75)
# Add red dot at global minima(s)
for gm in GLOBAL_MIN:
    ax2.plot(gm[0], gm[1], 'ro', markersize=3)

# Add labels
ax2.set_xlabel('$x_1$')
ax2.set_ylabel('$x_2$')
ax2.set_title('Contour Plot')

# Add color bar for contour plot
fig.colorbar(contour, ax=ax2, label="$f(x_1,x_2)$")

# Adjust layout
plt.tight_layout()

# Save Plot
plt.savefig(plotname)

# Show plot
plt.show()
