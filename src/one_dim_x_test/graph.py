#! /usr/bin/python3

##-------------------------------------------------------------------------------\
#   cat_swarm_python
#   '.src/one_dim_x_test/graph.py'
#   generates graphs for function based on constraints and configurations
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: June 24, 2024
##-------------------------------------------------------------------------------\


import numpy as np
import matplotlib.pyplot as plt

import configs_F as f_c
# problem constraints - pulled from the function configs for the optimizers
LOWER_BOUNDS = f_c.LB[0]
UPPER_BOUNDS = f_c.UB[0]
LB_x = LOWER_BOUNDS[0] 
UB_x = UPPER_BOUNDS[0]
FUNC_F = f_c.OBJECTIVE_FUNC
GLOBAL_MIN = f_c.GLOBAL_MIN

#write out plot
plotname = "1D_test_plots.png"

# Define range and step size
X = np.vstack(np.linspace(LB_x, UB_x, 1000))
# Reshape X to 1D array
X_flat = X.flatten()

# Evaluate function

Y = []
for c in X:
    y, noErr = FUNC_F(c)
    if noErr == True:
        Y.append(y)


# Create figure and subplots
fig = plt.figure(figsize=(10, 5))

# subplot
ax1 = fig.add_subplot(111)
surf = ax1.scatter(X,Y)
ax1.set_xlabel('$x_1$')
ax1.set_ylabel('$f(x_1)$')
ax1.set_title('Objective Function')

# Adjust layout
plt.tight_layout()

# Save Plot
plt.savefig(plotname)

# Show plot
plt.show()

