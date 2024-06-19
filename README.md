# sand_cat_python

Basic sand cat swarm optimizer written in Python following [2], and the MATLAB code provided via [mathworks sand cat swarm optimization](https://www.mathworks.com/matlabcentral/fileexchange/110185-sand-cat-swarm-optimization), [3].  The class structure is modified from the [adaptive timestep PSO optimizer](https://github.com/jonathan46000/pso_python) by [jonathan46000](https://github.com/jonathan46000) to keep a consistent format between optimizers in AntennaCAT.

Now featuring AntennaCAT hooks for GUI integration and user input handling.
 
## Table of Contents
* [Cat Swarm Optimization](#cat-swarm-optimization)
* [Sand Cat Swarm Optimization](#sand-cat-swarm-optimization)
* [Sand Cat Swarm Optimization Vs. Cat Swarm Optimization](#sand-cat-swarm-optimization-vs-cat-swarm-optimization)
    * [Cat Swarm Optimization (CSO)](#cat-swarm-optimization-cso)
    * [Sand Cat Swarm Optimization (SCSO)](#sand-cat-swarm-optimization-scso)
    * [Summary](#summary)
* [Requirements](#requirements)
* [Implementation](#implementation)
    * [Constraint Handling](#constraint-handling)
    * [Boundary Types](#boundary-types)
    * [Multi-Object Optimization](#multi-object-optimization)
    * [Objective Function Handling](#objective-function-handling)
      * [Internal Objective Function Example](internal-objective-function-example)
* [Examples](#example-implementations)
    * [Basic Swarm Example](#basic-swarm-example)
    * [Detailed Messages](#detailed-messages)
    * [Realtime Graph](#realtime-graph)
* [References](#references)
* [Publications and Integration](#publications-and-integration)
* [Licensing](#licensing)  

## Cat Swarm Optimization

Cat Swarm Optimization (CSO) is a nature-inspired optimization algorithm based on the behaviors of cats. It was introduced in "Cat Swarm Optimization" [1] in 2006. This algorithm resembles the traditional Particle Swarm Optimization (PSO) algorithm as it has location and velocity aspects, but the agents/particles in this algorithm have two options for movement in the update step. These two options are modeled off of two primary behaviors of cats: seeking and tracing. These modes represent the exploration and exploitation phases in optimization, respectively.

CSO divides the population of candidate solutions (cats) into two groups: one group for the seeking mode and another for the tracing mode. Each cat can switch between these modes according to a specified probability. 

1) Seeking Mode:

The seeking mode is responsible for exploring the search space to discover new and potentially better solutions. In this mode, cats simulate a behavior where they observe their surroundings and make decisions to move to new positions based on several possible moves. This helps the algorithm avoid getting stuck in local optima.

2) Tracing Mode:

The tracing mode is responsible for exploiting the search space by following the best solutions found so far. In this mode, cats simulate a behavior where they move towards a promising position, akin to a cat chasing prey. This helps refine solutions and converge towards the global optimum.

## Sand Cat Swarm Optimization

In [2] (A. Seyyedabbasi, 2023), Sand Cat Swarm Optimization (SCSO) was proposed as an algorithm able to escape local minima while retaining a balance between the exploitation and exploration. It has fewer parameters and operators than other metaheuristic algorithms, making it easier to implement than some swarm algorithm. 

There are two stages in foraging:

1) Exploitation:

This is the 'attacking prey' stage. In this stage, when an agent's position is updated, both random numbers and random thetas (from 0 to 360) are used to encourage movement out from the current location. The random position and next step are weighted by the global best to keep the exploitation constrained around the well-preforming locations.

2) Exploration:

This is the 'search' stage. In this stage, when evaluating the next location of each agent, a random cat is chosen from the group as a 'candidate', and that cat is used to move the current agent. This encourages the 'herd' behavior of the cats, rather than the motion being purely random.


## Sand Cat Swarm Optimization Vs. Cat Swarm Optimization

Cat Swarm Optimization (CSO) and Sand Cat Swarm Optimization (SCSO) are both nature-inspired optimization algorithms, but they are based on different behavioral models and have distinct mechanisms. Here are the key differences between the two:

### Cat Swarm Optimization (CSO)

**Inspiration**:

CSO is inspired by the behaviors of cats, particularly their seeking and tracing modes.

**Behavioral Modes**:

*Seeking Mode*: This mode mimics the cat's resting or exploring behavior. Cats in seeking mode explore the search space based on certain probabilities and selection mechanisms.

*Tracing Mode*: This mode mimics the cat's chasing or tracking behavior. Cats in tracing mode follow the best cat in the swarm, adjusting their position based on the velocity and best position information.

**Mechanism**:
* CSO alternates between seeking and tracing modes to balance exploration and exploitation.
* Parameters such as the seeking memory pool (SMP), seeking range of the selected dimension (SRD), counts of dimension to change (CDC), and self-position consideration (SPC) are used to control the seeking mode.
* Tracing mode uses velocity updates similar to Particle Swarm Optimization (PSO) but focuses on following the best position found.

### Sand Cat Swarm Optimization (SCSO)

**Inspiration**:

SCSO is inspired by the hunting and survival strategies of sand cats, which are well-adapted to desert environments.

**Behavioral Strategies**:
* SCSO incorporates specific strategies of sand cats related to hunting, such as stalking, pouncing, and other predatory behaviors.
* The algorithm may include mechanisms that simulate the cats' adaptation to the harsh desert environment, influencing how they explore and exploit the search space.

**Mechanism**:
* SCSO typically involves different phases that emulate the behavior of sand cats during hunting and survival.
* The algorithm uses adaptive mechanisms to balance exploration (searching new areas) and exploitation (refining known good areas).
* Velocity and position updates in SCSO might include elements inspired by the sand cats' efficient movement and energy conservation strategies.

### Summary 

Both CSO and SCSO aim to find optimal solutions by mimicking natural behaviors, but they differ in the specific animal behaviors they model and the strategies they use to balance exploration and exploitation of the search space.

| Aspect  | Cat Swarm Optimization (CSO) | Sand Cat Swarm Optimization (SCSO)|
| ------------- | ------------- |------------- |
| Inspiration  | General cat behavior (seeking and tracing)  | Sand cat's hunting and survival strategies |
| Behavioral Modes  | Seeking and Tracing modes  |Hunting and survival phases  |
| Mechanism  | Uses seeking memory pool, velocity updates, etc. | Adaptive strategies based on sand cat behavior |
| Exploration/Exploitation  | Alternates between seeking and tracing modes  |Balances using hunting and survival strategies  |
| Special Features | Parameters (e.g., SMP, SRD, CDC, SPC) for seeking mode  | Adaptive mechanisms inspired by sand cat movement  |

## Requirements

This project requires numpy and matplotlib. 

Use 'pip install -r requirements.txt' to install the following dependencies:

```python
contourpy==1.2.1
cycler==0.12.1
fonttools==4.51.0
importlib_resources==6.4.0
kiwisolver==1.4.5
matplotlib==3.8.4
numpy==1.26.4
packaging==24.0
pillow==10.3.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
six==1.16.0
zipp==3.18.1

```

## Implementation
### Constraint Handling
Users must create their own constraint function for their problems, if there are constraints beyond the problem bounds.  This is then passed into the constructor. If the default constraint function is used, it always returns true (which means there are no constraints).

### Boundary Types
This optimizer has 4 different types of bounds, Random (Particles that leave the area respawn), Reflection (Particles that hit the bounds reflect), Absorb (Particles that hit the bounds lose velocity in that direction), Invisible (Out of bound particles are no longer evaluated).

Some updates have not incorporated appropriate handling for all boundary conditions. This bug is known and is being worked on. The most consistent boundary type at the moment is Random.  If constraints are violated, but bounds are not, currently random bound rules are used to deal with this problem. 

### Multi-Object Optimization
The no preference method of multi-objective optimization, but a Pareto Front is not calculated. Instead, the best choice (smallest norm of output vectors) is listed as the output.

### Objective Function Handling
The optimizer minimizes the absolute value of the difference from the target outputs and the evaluated outputs. Future versions may include options for function minimization absent target values. 

#### Internal Objective Function Example
The current internal optimization function takes 3 inputs, and has 2 outputs. It was created as a simple 3-variable optimization objective function that would be quick to converge.  
<p align="center">
        <img src="https://github.com/LC-Linkous/cat_swarm_python/blob/sand_cat_python/media/obj_func_pareto.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
</p>
   <p align="center">Function Feasible Decision Space and Objective Space with Pareto Front</p>

```math
\text{minimize}: 
\begin{cases}
f_{1}(\mathbf{x}) = (x_1-0.5)^2 + (x_2-0.1)^2 \\
f_{2}(\mathbf{x}) = (x_3-0.2)^4
\end{cases}
```

| Num. Input Variables| Boundary | Constraints |
|----------|----------|----------|
| 3      | $0.21\leq x_1\leq 1$ <br> $0\leq x_2\leq 1$ <br> $0.1 \leq x_3\leq 0.5$  | $x_3\gt \frac{x_1}{2}$ or $x_3\lt 0.1$| 

This function has three files:
   1) configs_F.py - contains imports for the objective function and constraints, CONSTANT assignments for functions and labeling, boundary ranges, the number of input variables, the number of output values, and the target values for the output
   2) constr_F.py - contains a function with the problem constraints, both for the function and for error handling in the case of under/overflow. 
   3) func_F.py - contains a function with the objective function.

Other multi-objective functions can be applied to this project by following the same format (and several have been collected into a compatible library, and will be released in a separate repo)

## Example Implementations

### Basic Swarm Example
main_test.py provides a sample use case of the optimizer. 

### Detailed Messages
main_test_details.py provides an example using a parent class, and the self.suppress_output and detailedWarnings flags to control error messages that are passed back to the parent class to be printed with a timestamp. This implementation sets up the hooks for integration with AntennaCAT to provide the user feedback of warnings and errors.

### Realtime Graph

<p align="center">
        <img src="https://github.com/LC-Linkous/cat_swarm_python/blob/sand_cat_python/media/sand_cat_swarm.gif" alt="Example Sand Cat Swarm Optimization" height="200">
</p>

main_test_graph.py provides an example using a parent class, and the self.suppress_output and detailedWarnings flags to control error messages that are passed back to the parent class to be printed with a timestamp. Additionally, a realtime graph shows particle locations at every step. In this example, the cat swarm is not well-tuned to the problem and is not fast to converge, 
but the error from the target is relatively small.

NOTE: if you close the graph as the code is running, the code will continue to run, but the graph will not re-open.

## References

[1] S.-C. Chu, P. Tsai, and J.-S. Pan, “Cat Swarm Optimization,” Lecture Notes in Computer Science, pp. 854–858, 2006, doi: https://doi.org/10.1007/978-3-540-36668-3_94.

[2] A. Seyyedabbasi and F. Kiani, “Sand Cat swarm optimization: a nature-inspired algorithm to solve global optimization problems,” Engineering with Computers, Apr. 2022, doi: https://doi.org/10.1007/s00366-022-01604-x.

[3] “Sand Cat swarm optimization,” www.mathworks.com. https://www.mathworks.com/matlabcentral/fileexchange/110185-sand-cat-swarm-optimization (accessed Jun. 19, 2024).

[4] J. G. March, “Exploration and Exploitation in Organizational Learning,” Organization Science, vol. 2, no. 1, pp. 71–87, Feb. 1991, doi: https://doi.org/10.1287/orsc.2.1.71.  (Bonus read of where the 'exploration and exploitation' phrase often comes from)

## Publications and Integration
This software works as a stand-alone implementation, and as one of the optimizers integrated into AntennaCAT.

Publications featuring the code in this repo will be added as they become public.

## Licensing

The code in this repository has been released under GPL-2.0



