#! /usr/bin/python3

##-------------------------------------------------------------------------------\
#   cat_swarm_quantum
#   './cat_swarm_quantum/src/main_function_graph.py'
#   generates graphs for function based on constraints and configurations
#   in-package demo for graphing the pareto front
#
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: June 4, 2024
##-------------------------------------------------------------------------------\

import numpy as np
import matplotlib.pyplot as plt

import configs_F as f_c
# problem constraints - pulled from the function configs for the optimizers
LOWER_BOUNDS = f_c.LB[0]
UPPER_BOUNDS = f_c.UB[0]
LB_x = LOWER_BOUNDS[0]
UB_x = UPPER_BOUNDS[0] 
LB_y = LOWER_BOUNDS[1]
UB_y = UPPER_BOUNDS[1]
LB_z = LOWER_BOUNDS[2]
UB_z = UPPER_BOUNDS[2]
IN_VARS = f_c.IN_VARS
FUNC_F = f_c.OBJECTIVE_FUNC
CONSTR_F = f_c.CONSTR_FUNC

def pareto_front(X, Y, minimize=True):
    pareto_front_X = []
    pareto_front_Y = []

    if minimize:
        # Find Pareto front for minimizing objectives
        pareto_front_Y_max = float('inf')
        for x, y in sorted(zip(X, Y)):
            if y < pareto_front_Y_max:
                pareto_front_X.append(x)
                pareto_front_Y.append(y)
                pareto_front_Y_max = y
    else:
        # Find Pareto front for maximizing objectives
        pareto_front_Y_min = float('-inf')
        for x, y in sorted(zip(X, Y), reverse=True):
            if y > pareto_front_Y_min:
                pareto_front_X.append(x)
                pareto_front_Y.append(y)
                pareto_front_Y_min = y

    return pareto_front_X, pareto_front_Y



# Define range and step size
x = np.linspace(LB_x, UB_x, 100)
y = np.linspace(LB_y, UB_y, 100)
z = np.linspace(LB_z, UB_z, 100)

x_grid = np.array(np.meshgrid(x, y, z)).T.reshape(-1, IN_VARS) 

# Evaluate function + apply constraints
# this is the same function used by the optimizers, so the format reflects that
validCoords = [] # the valid x,y coordinates
paretoCoords = [] #col1: f1, col2: f2
for c in x_grid:
    # check if point is in the constraints.
    point_is_valid = CONSTR_F(c)
    if point_is_valid == True:
        # add point to validCoords
        validCoords.append(c)
        # pass point to the function to get the minimized F set
        objective_space, noErr = FUNC_F(c)
        if noErr == True:
            paretoCoords.append(objective_space)


# Convert validCoords to a NumPy array
validCoords = np.array(validCoords)
valid_x = validCoords[:,0]
valid_y = validCoords[:,1]
valid_z = validCoords[:,2]

# Convert paretoCoords to a NumPy array
paretoCoords = np.array(paretoCoords)

# Get the feasible objective space
objective_x = paretoCoords[:,0]
objective_y = paretoCoords[:,1]
# Get the Pareto front from the feasible objective space
pareto_x, pareto_y = pareto_front(objective_x,objective_y)

# Create figure and subplots
fig = plt.figure(figsize=(14, 7))

# 2D valid state space subplot - dimensionality reduction
ax1 = fig.add_subplot(121, projection='3d')
decision_space = ax1.tricontourf(valid_x, valid_y, valid_z, cmap='viridis')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')
ax1.set_title('Feasible Decision Space')


# 2D valid objective space subplot
ax2 = fig.add_subplot(122)
# check if the objective space is all pareto optimal
if len(pareto_x) < 1:
    # the objective space on this problem IS the Pareto front
    objective_space = ax2.scatter(objective_x.flatten(), objective_y.flatten(), color='c')
    ax2.scatter(objective_x.flatten(), objective_y.flatten(), marker='*', color='black')
else: # not pareto optimal
    objective_space = ax2.scatter(objective_x.flatten(), objective_y.flatten(), color='c')
    ax2.scatter(pareto_x, pareto_y, marker='*', color='black')

ax2.set_xlabel('$f_{1}(x,y)$')
ax2.set_ylabel('$f_{2}(x,y)$')
ax2.set_title('Pareto Front & Feasible Objective Space')


# Adjust layout
plt.tight_layout()

# Show plot
plt.show()
