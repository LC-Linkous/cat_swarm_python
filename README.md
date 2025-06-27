# cat_swarm_quantum

A 'quantum' cat swarm optimizer written in Python using quantum inspired methods (non-qiskit). Modified from the [adaptive timestep PSO optimizer](https://github.com/jonathan46000/pso_python) by [jonathan46000](https://github.com/jonathan46000) to keep a consistent format between optimizers in AntennaCAT.


Now featuring AntennaCAT hooks for GUI integration and user input handling.

This branch of the repository is part of a series of replication studies. It is not intended to be the 'best' implementation, or the most recent advancement of the algorithm. This method has been chosen to replicate a specific snapshot of literature.


## Table of Contents
* [Cat Swarm Optimization](#cat-swarm-optimization)
* [Quantum Inspired Optimization](#quantum-inspired-optimization)
* [Quantum Cat Swarm Optimization](#quantum-cat-swarm-optimization)
    * [Quantum Seeking Mode](#quantum-seeking-mode)
       * [Mean Best Position](#mean-best-position)
       * [Position Update](#position-update)
* [Requirements](#requirements)
* [Implementation](#implementation)
    * [Initialization](#initialization) 
    * [State Machine-based Structure](#state-machine-based-structure)
    * [Importing and Exporting Optimizer State](#importing-and-exporting-optimizer-state)
    * [Constraint Handling](#constraint-handling)
    * [Boundary Types](#boundary-types)
    * [Multi-Objective Optimization](#multi-objective-optimization)
    * [Objective Function Handling](#objective-function-handling)
      * [Creating a Custom Objective Function](#creating-a-custom-objective-function)
      * [Internal Objective Function Example](internal-objective-function-example)
      * [Target vs. Threshold Configuration](#target-vs-threshold-configuration)
* [Examples](#example-implementations)
    * [Basic Swarm Example](#basic-swarm-example)
    * [Detailed Messages](#detailed-messages)
    * [Realtime Graph](#realtime-graph)
* [References](#references)
* [Related Publications and Repositories](#related-publications-and-repositories)
* [Licensing](#licensing)  

## Cat Swarm Optimization

Cat Swarm Optimization (CSO) is a nature-inspired optimization algorithm based on the behaviors of cats. It was introduced in "Cat Swarm Optimization" [1] in 2006. This algorithm resembles the traditional Particle Swarm Optimization (PSO) algorithm as it has location and velocity aspects, but the agents/particles in this algorithm have two options for movement in the update step. These two options are modeled off of two primary behaviors of cats: seeking and tracing. These modes represent the exploration and exploitation phases in optimization, respectively.

CSO divides the population of candidate solutions (cats) into two groups: one group for the seeking mode and another for the tracing mode. Each cat can switch between these modes according to a specified probability. 

1) Seeking Mode:

The seeking mode is responsible for exploring the search space to discover new and potentially better solutions. In this mode, cats simulate a behavior where they observe their surroundings and make decisions to move to new positions based on several possible moves. This helps the algorithm avoid getting stuck in local optima.

2) Tracing Mode:

The tracing mode is responsible for exploiting the search space by following the best solutions found so far. In this mode, cats simulate a behavior where they move towards a promising position, akin to a cat chasing prey. This helps refine solutions and converge towards the global optimum.


## Quantum Inspired Optimization

Quantum(-inspired) Particle Swarm Optimization (QPSO) was introduced in 2004 [2] [3]. Paraphrased from [2], in PSO the location and velocity vectors are used to determine the trajectory of the particle, which because in Newtonian mechanics a particle moves along a determined trajectory. However, in quantum mechanics, the location and velocity vectors cannot be determined/known simultaneously due to uncertainty principle (Werner Heisenberg, 1927). The takeaway being, quantum-inspired algorithms take concepts from quantum mechanics, such as superposition and entanglement, and apply them in classical computation to solve optimization problems more effectively (depending on the problem type). 

These two concepts are applied, generally speaking, as follows:


1) Superposition

**Quantum Concept**: In quantum mechanics, a particle canexist in a superposition of multiple states simultaneously. For example, a quantum bit (qubit) can be in a state ∣0⟩∣0⟩, ∣1⟩∣1⟩, or any linear combination ∣ψ⟩=α∣0⟩+β∣1⟩∣ψ⟩=α∣0⟩+β∣1⟩, where α and β are complex numbers.

**Classical Adaptation**: In quantum-inspired algorithms, superposition can be interpreted as a probability distribution over multiple states. Instead of particles having a single position, they are represented by a probability distribution, reflecting the potential to be in various positions simultaneously.

**Example in QPSO**: In the Quantum-inspired Particle Swarm Optimization (QPSO), a particle’s position is often updated using a probability distribution derived from both personal best and global best positions, rather than a deterministic position update. This allows particles to explore the search space more effectively.


2) Entanglement

**Quantum Concept**: Entanglement is a phenomenon where particles become interconnected such that the state of one particle directly affects the state of another, no matter the distance between them. This creates a strong correlation between the particles.

**Classical Adaptation**: In quantum-inspired algorithms, entanglement can be represented as a dependency or correlation between particles. When one particle updates its position, it influences the position updates of other particles, promoting cooperative behavior among the particles in the swarm.

**Example in QPSO**: In QPSO, the positions of particles might be updated using a combination of their personal best position and the global best position, creating a form of "entanglement" where particles are influenced by the best solutions found by the swarm, thus maintaining a level of coordination and cooperation.



## Quantum Cat Swarm Optimization

Unlike traditional PSO, quantum-inspired swarm optimization algorithms don't use paired position and velocity vectors. Instead, they generally update particle positions directly based on a probability distribution based on the mean best position and a logarithmic factor, which has roots in the quantum mechanics principles mentioned previously. The QPSO update rule leverages quantum-inspired probabilistic movements to balance exploration and exploitation. By combining the best aspects of personal and global experiences and adding a stochastic component, QPSO can effectively search complex optimization landscapes. 


### Quantum Seeking Mode

*  Generates several copies of the cat's position using a quantum-inspired update rule, which involves:
  * Calculating a mean best position, $mb$, as a combination of the global best position, $g$, and the current cat's position, $p$.
  * Introducing a probabilistic factor, $u$, to generate new positions.
  * Evaluates the fitness of these new positions and selects the best one.

#### Mean Best Position
 
Mean Best Position ($mb$) is a weighted average of the personal best position ($p$) and the global best position ($g$). It is calculated as:

```math
mb=\beta \cdot p+(1−\beta) \cdot g

```

Where:

* $\beta$ is a parameter controlling the influence between the personal and global best positions.

#### Position Update

 In QPSO, instead of updating the velocity and then the position, we directly update the position using quantum mechanics-inspired rules. The update rule is:

```math
x_i(t+1) = mb \pm \beta \cdot \lvert p - g \rvert \cdot \log(1/u)
```

Where:

* $mb$ is the mean best position
* $\beta$ is a user-defined parameter influencing convergence behavior.
* $p$ is the personal best position of the particle.
* $g$ is the global best position of the swarm.
* $u$ is a uniformly distributed random number in the range (0, 1).
* The logarithmic term $log(1/u)$ comes from the distribution properties of quantum systems.
* $\beta \cdot \lvert p−g \rvert $ scales the exploration step based on the distance between the personal and global best positions.
* $log(1/u)$ introduces a random factor with a bias towards smaller values (since $u$ is between 0 and 1, $log(1/u)$ is negative, making $−log⁡(1/u)$ positive).


The QPSO update rule is based on the quantum mechanics principle where particles have a probability distribution of being in different positions. The position update rule can be seen as a way to explore the search space more effectively through 2 key factors:

**Diverse Exploration**: The term $log⁡(1/u_2)$ helps in creating a wide range of possible moves, allowing the particles to explore the search space extensively. The logarithmic function is chosen because it provides a heavy-tailed distribution, meaning particles can make both small and large jumps, avoiding local minima and encouraging global exploration.

**Balanced Exploitation**: The combination of $mb$, $p$, and $g$ ensures that the particles are guided towards promising regions of the search space, leveraging both individual experience (personal_best) and collective knowledge (global_best).



### Quantum Tracing Mode

Update the cat’s position towards the global best position using the quantum-inspired probabilistic update rule, in this case the random vector $u$.



## Requirements

This project requires numpy, pandas, and matplotlib for the full demos. To run the optimizer without visualization, only numpy and pandas are requirements

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
pandas==2.2.3
pillow==10.3.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
pytz==2025.1
six==1.16.0
tzdata==2025.1
zipp==3.18.1

```

Optionally, requirements can be installed manually with:

```python
pip install  matplotlib, numpy, pandas

```
This is an example for if you've had a difficult time with the requirements.txt file. Sometimes libraries are packaged together.


## Implementation
### Initialization 

```python
    # Constant variables
    NO_OF_PARTICLES = 50         # Number of particles in swarm
    #WEIGHTS = [[2, 2.2, 2]]
    WEIGHTS = [[2, 2.2]]         # Update vector weights. Used as C1 constant in tracing mode.
                                    # NOTE: the weight vector MUST have the same shape as the LB 
                                    # and UB. 
    TOL = 10 ** -6               # Convergence Tolerance
    MAXIT = 5000                 # Maximum allowed iterations
    BOUNDARY = 1                 # int boundary 1 = random,      2 = reflecting
                                 #              3 = absorbing,   4 = invisible
    
    # Objective function dependent variables
    LB = func_configs.LB                    # Lower boundaries, [[0.21, 0, 0.1]]
    UB = func_configs.UB                    # Upper boundaries, [[1, 1, 0.5]]
    IN_VARS = func_configs.IN_VARS          # Number of input variables (x-values)   
    OUT_VARS = func_configs.OUT_VARS        # Number of output variables (y-values)
    TARGETS = func_configs.TARGETS          # Target values for output

    # Objective function dependent variables
    func_F = func_configs.OBJECTIVE_FUNC  # objective function
    constr_F = func_configs.CONSTR_FUNC   # constraint function

    # cat swarm specific
    MR = .02                    # Mixture Ratio (MR). Small value for tracing population %.
    SMP = 5                     # Seeking memory pool. Num copies of cats made.
    SRD = .45                   # Seeking range of the selected dimension. 
    CDC = 2                     # Counts of dimension to change. mutation.
    SPC = True                  # self-position consideration. boolean.

    # quantum swarm variables
    BETA = 0.5                  #Float constant controlling influence 
                                    #between the personal and global best positions


    # swarm setup
    best_eval = 1
    parent = None            
    suppress_output = True   # Suppress the console output of particle swarm
    allow_update = True      # Allow objective call to update state 

    # Constant variables
    opt_params = {'NO_OF_PARTICLES': [NO_OF_PARTICLES],     # Number of particles in swarm
                'BOUNDARY': [BOUNDARY],                     # int boundary 1 = random,      2 = reflecting
                                                            #              3 = absorbing,   4 = invisible
                'WEIGHTS': [WEIGHTS],                       # Update vector weights
                'MR': [MR],                                 # Mixture Ratio (MR). Small value for tracing population %.
                'SMP': [SMP],                               # Seeking memory pool. Num copies of cats made.
                'SRD': [SRD],                               # Seeking range of the selected dimension. 
                'CDC': [CDC],                               # Counts of dimension to change. mutation.
                'SPC': [SPC],                               # self-position consideration. boolean.
                'BETA': [BETA] }                            # Float constant controlling influence 
                                                            #     between the personal and global best positions
    
    opt_df = pd.DataFrame(opt_params)
    mySwarm = swarm(LB, UB, TARGETS, TOL, MAXIT,
                            func_F, constr_F,
                            opt_df,
                            parent=parent, 
                            evaluate_threshold=False, obj_threshold=None,
                            decimal_limit = 4)

    # arguments should take the form: 
    # swarm([[float, float, ...]], [[float, float, ...]], [[float, ...]], float, int,
    # func, func,
    # dataFrame,
    # class obj, 
    # bool, [int, int, ...], 
    # int) 
    #  
    # opt_df contains class-specific tuning parameters
    # NO_OF_PARTICLES: int
    # weights: [[float, float, float]]
    # boundary: int. 1 = random, 2 = reflecting, 3 = absorbing,   4 = invisible
    # MR: float. Small value
    # SMP: int
    # SRD: float
    # CDC: int
    # SPC: bool
    #             
```

### State Machine-based Structure

This optimizer uses a state machine structure to control the movement of the particles, call to the objective function, and the evaluation of current positions. The state machine implementation preserves the initial algorithm while making it possible to integrate other programs, classes, or functions as the objective function.

A controller with a `while loop` to check the completion status of the optimizer drives the process. Completion status is determined by at least 1) a set MAX number of iterations, and 2) the convergence to a given target using the L2 norm.  Iterations are counted by calls to the objective function. 

Within this `while loop` are three function calls to control the optimizer class:
* **complete**: the `complete function` checks the status of the optimizer and if it has met the convergence or stop conditions.
* **step**: the `step function` takes a boolean variable (suppress_output) as an input to control detailed printout on current particle (or agent) status. This function moves the optimizer one step forward.  
* **call_objective**: the `call_objective function` takes a boolean variable (allow_update) to control if the objective function is able to be called. In most implementations, this value will always be true. However, there may be cases where the controller or a program running the state machine needs to assert control over this function without stopping the loop.

Additionally, **get_convergence_data** can be used to preview the current status of the optimizer, including the current best evaluation and the iterations.

The code below is an example of this process:

```python
    while not myOptimizer.complete():
        # step through optimizer processing
        # this will update particle or agent locations
        myOptimizer.step(suppress_output)
        # call the objective function, control 
        # when it is allowed to update and return 
        # control to optimizer
        myOptimizer.call_objective(allow_update)
        # check the current progress of the optimizer
        # iter: the number of objective function calls
        # eval: current 'best' evaluation of the optimizer
        iter, eval = myOptimizer.get_convergence_data()
        if (eval < best_eval) and (eval != 0):
            best_eval = eval
        
        # optional. if the optimizer is not printing out detailed 
        # reports, preview by checking the iteration and best evaluation

        if suppress_output:
            if iter%100 ==0: #print out every 100th iteration update
                print("Iteration")
                print(iter)
                print("Best Eval")
                print(best_eval)
```

### Importing and Exporting Optimizer State

Some optimizer information can be exported or imported. This varies based on each optimizer.

Optimizer state can be exported at any step. When importing an optimizer state, the optimizer should be initialized first, and then the state information can be imported via a Python pickle file. Other methods can be used if custom code is written to handle preprocessing.


Returning data from optimizer and saving to a .pkl file:
```python
    data = demo_optimizer.export_swarm()
    data_df = pd.DataFrame(data)
    print(data_df)
    data_df.to_pickle('output_data_df.pkl')

```


Importing data from a .pkl file and importing it into the optimizer:
```python
    data_df = pd.read_pickle('output_data_df.pkl') 
    demo_optimizer.import_swarm(data_df)

```


### Constraint Handling
Users must create their own constraint function for their problems, if there are constraints beyond the problem bounds.  This is then passed into the constructor. If the default constraint function is used, it always returns true (which means there are no constraints).

### Boundary Types
This optimizer has 4 different types of bounds, Random (Particles that leave the area respawn), Reflection (Particles that hit the bounds reflect), Absorb (Particles that hit the bounds lose velocity in that direction), Invisible (Out of bound particles are no longer evaluated).

Some updates have not incorporated appropriate handling for all boundary conditions. This bug is known and is being worked on. The most consistent boundary type at the moment is Random.  If constraints are violated, but bounds are not, currently random bound rules are used to deal with this problem. 

### Multi-Objective Optimization
The no preference method of multi-objective optimization, but a Pareto Front is not calculated. Instead, the best choice (smallest norm of output vectors) is listed as the output.


### Objective Function Handling

The objective function is handled in two parts. 


* First, a defined function, such as one passed in from `func_F.py` (see examples), is evaluated based on current particle locations. This allows for the optimizers to be utilized in the context of 1. benchmark functions from the objective function library, 2. user defined functions, 3. replacing explicitly defined functions with outside calls to programs such as simulations or other scripts that return a matrix of evaluated outputs. 

* Secondly, the actual objective function is evaluated. In the AntennaCAT set of optimizers, the objective function evaluation is either a `TARGET` or `THRESHOLD` evaluation. For a `TARGET` evaluation, which is the default behavior, the optimizer minimizes the absolute value of the difference of the target outputs and the evaluated outputs. A `THRESHOLD` evaluation includes boolean logic to determine if a 'greater than or equal to' or 'less than or equal to' or 'equal to' relation between the target outputs (or thresholds) and the evaluated outputs exist. 

Future versions may include options for function minimization when target values are absent. 



#### Creating a Custom Objective Function

Custom objective functions can be used by creating a directory with the following files:
* configs_F.py
* constr_F.py
* func_F.py

`configs_F.py` contains lower bounds, upper bounds, the number of input variables, the number of output variables, the target values, and a global minimum if known. This file is used primarily for unit testing and evaluation of accuracy. If these values are not known, or are dynamic, then they can be included experimentally in the controller that runs the optimizer's state machine. 

`constr_F.py` contains a function called `constr_F` that takes in an array, `X`, of particle positions to determine if the particle or agent is in a valid or invalid location. 

`func_F.py` contains the objective function, `func_F`, which takes two inputs. The first input, `X`, is the array of particle or agent positions. The second input, `NO_OF_OUTS`, is the integer number of output variables, which is used to set the array size. In included objective functions, the default value is hardcoded to work with the specific objective function.

Below are examples of the format for these files.

`configs_F.py`:
```python
OBJECTIVE_FUNC = func_F
CONSTR_FUNC = constr_F
OBJECTIVE_FUNC_NAME = "one_dim_x_test.func_F" #format: FUNCTION NAME.FUNCTION
CONSTR_FUNC_NAME = "one_dim_x_test.constr_F" #format: FUNCTION NAME.FUNCTION

# problem dependent variables
LB = [[0]]             # Lower boundaries
UB = [[1]]             # Upper boundaries
IN_VARS = 1            # Number of input variables (x-values)
OUT_VARS = 1           # Number of output variables (y-values) 
TARGETS = [0]          # Target values for output
GLOBAL_MIN = []        # Global minima sample, if they exist. 

```

`constr_F.py`, with no constraints:
```python
def constr_F(x):
    F = True
    return F
```

`constr_F.py`, with constraints:
```python
def constr_F(X):
    F = True
    # objective function/problem constraints
    if (X[2] > X[0]/2) or (X[2] < 0.1):
        F = False
    return F
```

`func_F.py`:
```python
import numpy as np
import time

def func_F(X, NO_OF_OUTS=1):
    F = np.zeros((NO_OF_OUTS))
    noErrors = True
    try:
        x = X[0]
        F = np.sin(5 * x**3) + np.cos(5 * x) * (1 - np.tanh(x ** 2))
    except Exception as e:
        print(e)
        noErrors = False

    return [F], noErrors
```


#### Internal Objective Function Example

There are three functions included in the repository:
1) Himmelblau's function, which takes 2 inputs and has 1 output
2) A multi-objective function with 3 inputs and 2 outputs (see lundquist_3_var)
3) A single-objective function with 1 input and 1 output (see one_dim_x_test)

Each function has four files in a directory:
   1) configs_F.py - contains imports for the objective function and constraints, CONSTANT assignments for functions and labeling, boundary ranges, the number of input variables, the number of output values, and the target values for the output
   2) constr_F.py - contains a function with the problem constraints, both for the function and for error handling in the case of under/overflow. 
   3) func_F.py - contains a function with the objective function.
   4) graph.py - contains a script to graph the function for visualization.

Other multi-objective functions can be applied to this project by following the same format (and several have been collected into a compatible library, and will be released in a separate repo)

<p align="center">
        <img src="media/himmelblau_plots.png" alt="Himmelblau’s function" height="250">
</p>
   <p align="center">Plotted Himmelblau’s Function with 3D Plot on the Left, and a 2D Contour on the Right</p>

```math
f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2
```

| Global Minima | Boundary | Constraints |
|----------|----------|----------|
| f(3, 2) = 0                 | $-5 \leq x,y \leq 5$  |   | 
| f(-2.805118, 3.121212) = 0  | $-5 \leq x,y \leq 5$  |   | 
| f(-3.779310, -3.283186) = 0 | $-5 \leq x,y \leq 5$  |   | 
| f(3.584428, -1.848126) = 0  | $-5 \leq x,y \leq 5$   |   | 

<p align="center">
        <img src="media/obj_func_pareto.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
</p>
   <p align="center">Plotted Multi-Objective Function Feasible Decision Space and Objective Space with Pareto Front</p>

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

<p align="center">
        <img src="media/1D_test_plots.png" alt="Function Feasible Decision Space and Objective Space with Pareto Front" height="200">
</p>
   <p align="center">Plotted Single Input, Single-objective Function Feasible Decision Space and Objective Space with Pareto Front</p>

```math
f(\mathbf{x}) = sin(5 * x^3) + cos(5 * x) * (1 - tanh(x^2))
```
| Num. Input Variables| Boundary | Constraints |
|----------|----------|----------|
| 1      | $0\leq x\leq 1$  | $0\leq x\leq 1$| |

Local minima at $(0.444453, -0.0630916)$

Global minima at $(0.974857, -0.954872)$


### Target vs. Threshold Configuration

An April 2025 feature is the user ability to toggle TARGET and THRESHOLD evaluation for the optimized values. The key variables for this are:

```python
# Boolean. use target or threshold. True = THRESHOLD, False = EXACT TARGET
evaluate_threshold = True  

# array
TARGETS = func_configs.TARGETS    # Target values for output from function configs
# OR:
TARGETS = [0,0,0] #manually set BASED ON PROBLEM DIMENSIONS

# threshold is same dims as TARGETS
# 0 = use target value as actual target. value should EQUAL target
# 1 = use as threshold. value should be LESS THAN OR EQUAL to target
# 2 = use as threshold. value should be GREATER THAN OR EQUAL to target
#DEFAULT THRESHOLD
THRESHOLD = np.zeros_like(TARGETS) 
# OR
THRESHOLD = [0,1,2] # can be any mix of TARGET and THRESHOLD  
```

To implement this, the original `self.Flist` objective function calculation has been replaced with the function `objective_function_evaluation`, which returns a numpy array.

The original calculation:
```python
self.Flist = abs(self.targets - self.Fvals)
```
Where `self.Fvals` is a re-arranged and error checked returned value from the passed in function from `func_F.py` (see examples for the internal objective function or creating a custom objective function). 

When using a THRESHOLD, the `Flist` value corresponding to the target is set to epsilon (the smallest system value) if the evaluated `func_F` value meets the threshold condition for that target item. If the threshold is not met, the absolute value of the difference of the target output and the evaluated output is used. With a THRESHOLD configuration, each value in the numpy array is evaluated individually, so some values can be 'greater than or equal to' the target while others are 'equal' or 'less than or equal to' the target. 




## Example Implementations

### Basic Swarm Example
`main_test.py` provides a sample use case of the optimizer. 

### Detailed Messages
`main_test_details.py` provides an example using a parent class, and the self.suppress_output flag to control error messages that are passed back to the parent class to be printed with a timestamp. This implementation sets up the hooks for integration with AntennaCAT to provide the user feedback of warnings and errors.

### Realtime Graph

<p align="center">
        <img src="/media/qcat_swarm.gif" alt="Example Quantum Cat Swarm Optimization" height="200">
</p>

`main_test_graph.py` provides an example using a parent class, and the self.suppress_output flag to control error messages that are passed back to the parent class to be printed with a timestamp. Additionally, a realtime graph shows particle locations at every step. 

NOTE: if you close the graph as the code is running, the code will continue to run, but the graph will not re-open.

## References

[1] S.-C. Chu, P. Tsai, and J.-S. Pan, “Cat Swarm Optimization,” Lecture Notes in Computer Science, pp. 854–858, 2006, doi: https://doi.org/10.1007/978-3-540-36668-3_94.


[2] Jun Sun, Bin Feng and Wenbo Xu, "Particle swarm optimization with particles having quantum behavior," Proceedings of the 2004 Congress on Evolutionary Computation (IEEE Cat. No.04TH8753), Portland, OR, USA, 2004, pp. 325-331 Vol.1, doi: 10.1109/CEC.2004.1330875.

[3] Jun Sun, Wenbo Xu and Bin Feng, "A global search strategy of quantum-behaved particle swarm optimization," IEEE Conference on Cybernetics and Intelligent Systems, 2004., Singapore, 2004, pp. 111-116 vol.1, doi: 10.1109/ICCIS.2004.1460396.

[4] X. Nie, W. Wang, and H. Nie, “Chaos Quantum-Behaved Cat Swarm Optimization Algorithm and Its Application in the PV MPPT,” Computational Intelligence and Neuroscience, vol. 2017, pp. 1–11, Jan. 2017, doi: https://doi.org/10.1155/2017/1583847.

[5] A. M. Ahmed, T. A. Rashid, and S. Ab. M. Saeed, “Cat Swarm Optimization Algorithm: A Survey and Performance Evaluation,” Computational Intelligence and Neuroscience, vol. 2020, pp. 1–20, Jan. 2020, doi: https://doi.org/10.1155/2020/4854895.

## Related Publications and Repositories
This software works as a stand-alone implementation, and as one of the optimizers integrated into AntennaCAT.


## Licensing

The code in this repository has been released under GPL-2.0


