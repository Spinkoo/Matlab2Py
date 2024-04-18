# Matlab2Py
Python interface with Matlab simulations at <b>Runtime</b>



## Matlab engine (`mat_engine.py`)
`mat_engine.py` is a Python controller. It is an interface that connects a Python environment to a Matlab simulation, allowing for the execution of Matlab scripts and the retrieval of simulation data directly from Python during Runtime with different modes.

# Matlab Engine Wrapper for Python

This repository contains a Python wrapper for the MATLAB Engine API, designed to facilitate the integration of MATLAB simulations into Python applications. The primary component of this repository is the `Engine` class, which provides a high-level interface for controlling MATLAB simulations from Python. This README provides an overview of the repository's functionality and explains the parameters used by the `Engine` class.

## Overview

The `Engine` class is designed to abstract away the complexities of interacting with MATLAB simulations, allowing Python developers to control and manipulate MATLAB simulations with ease. It provides methods for starting, pausing, stepping through, and stopping simulations, as well as accessing and modifying simulation parameters.

### Interface mode 

The simulation parameters and signals can be accessed through three modes : 

- `'sbs'`: Step by Step simulation. This mode allows for detailed control over the simulation, stepping through it one step at a time.
- `'sparsesbs'`: Sparse Step by Step simulation. This mode skips certain steps if they are deemed unnecessary, potentially speeding up the simulation.
- `'normal'`: Normal simulation mode. This mode runs the simulation without any step-by-step control and the results should be retrived by the user afterwards. 
## Setup 

[Install Matlab engine for Python](https://fr.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-engine-for-python.html)

Run ```python -m pip install -r requirements.txt```
## Engine Parameters

The `Engine` class constructor accepts several parameters that configure its behavior. Here's a brief explanation of each:

- `model_path`: The path to the MATLAB model file (.slx file) that contains the simulation to be controlled.
- `sim_path`: The path to the directory containing the simulation files. This is where the MATLAB Engine will look for the model file and any other necessary files.
- `model_name` (default: 'Trolley'): The name of the MATLAB model to be loaded. This is used to reference the model within the MATLAB Engine.
- `matlab_stepper` (default: 'step_time'): The name of the MATLAB block that controls the simulation's step size. This is used to advance the simulation one step at a time ([See How to set a stepper](#matlab-stepper)).
- `simulation_type` (default: 'sbs'): The type of simulation to run. The supported types are:
    - `'sbs'`: Step by Step simulation. This mode allows for detailed control over the simulation, stepping through it one step at a time.
    - `'sparsesbs'`: Sparse Step by Step simulation. This mode skips certain steps if they are deemed unnecessary, potentially speeding up the simulation.
    - `'normal'`: Normal simulation mode. This mode runs the simulation without any step-by-step control and the results should be retrived by the user afterwards.
- `max_steps`: This parameter sets the maximum number of steps for the simulation. It acts as a sort of timeout, preventing the simulation from running indefinitely. This is particularly useful in scenarios where you want to limit the simulation to a certain number of iterations for testing or debugging purposes([See How to set a timeout](#matlab-timeout)).


## Usage

To use the `Engine` class, you first need to create an instance of the class, passing the appropriate parameters to the constructor. Once the instance is created, you can use its methods to control the simulation. Here's a basic example:

```from mat_engine import Engine

Initialize the engine with the path to the model and simulation files
engine = Engine(model_path='path/to/model.slx', sim_path='path/to/simulation/files')

#Set parameters

Load the simulation
engine.load_engine()

Start the simulation
engine.start_simulation()

Pause the simulation
engine.pause_simulation()

Step through the simulation
engine.step_forward()

Stop the simulation
engine.stop_simulation()
```

# Setup Timeout and Stepper blocks in Matlab
![](images/interface_block.png)

## Matlab timeout
The simplest way to set a tuneable timeout is to add a binary comparison block connected to your clock that'll be periodically compared to the max_sim_time (the name of the variable can be set progrmatically if you prefer otherwise)

## Matlab Stepper

Matlab Stepper allows to run through the simulation at specific time intervales and provides access to the Simulation variables during Runtime at sparse intervales (every `step_time`) rather than step by step iterations which can be very superfluous and overkill. This is done by adding an assertion block like in the figure; 

Note that it is necessary to set the following parameters in the assertion block (double click on the block ): Simulation callback when assertion fail = `set_param(bdroot,'SimulationCommand','pause')`

# Example
An example using a functioning simulation can be viewed in [Thimyo training using RL](https://github.com/Spinkoo/Matlab2TorchRL/blob/main/gyms/envs/Matlab2Py/test.py)