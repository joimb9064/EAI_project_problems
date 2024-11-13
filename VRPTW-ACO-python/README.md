
# VRPTW Ant Colony Optimization (ACO)

This project is an implementation of the Ant Colony Optimization (ACO) algorithm for solving the Vehicle Routing Problem with Time Windows (VRPTW). The algorithm employs a colony of ants to find optimized paths for a fleet of vehicles, considering customer time constraints.

## Project Structure

The primary files are:

- **`ant.py`**: Defines the `Ant` class, which represents an individual ant in the ACO algorithm. Each ant searches for a path that minimizes the total route cost.
- **`basic_aco.py`**: Contains the `BasicACO` class, which sets up and manages the ACO algorithm, handling multiple ants and iterations.
- **`vprtw_aco_figure.py`**: Provides visualization utilities for the VRPTW solutions using matplotlib.
- **`vrptw_base.py`**: Defines foundational classes and data structures for VRPTW, such as `Node` and `VrptwGraph`.
- **`ACO_main_script.py`**: The main script for running the ACO algorithm on VRPTW data. Configures and initiates the optimization process.

## Requirements

To use these scripts, ensure that the following Python packages are installed:

- `numpy`
- `matplotlib`

You can install these dependencies with:
```bash
pip install numpy matplotlib
```

## Setup and Usage

1. **Download or Clone the Project**  
   Place all the files (`ant.py`, `basic_aco.py`, `vprtw_aco_figure.py`, `vrptw_base.py`, `ACO_main_script.py`) in the same directory.

2. **Prepare Data**  
   The `ACO_main_script.py` requires a VRPTW data file, such as `c101.txt`, which should be structured according to Solomon's VRPTW format. Place this file in the designated directory, or update the path in `ACO_main_script.py` accordingly.

3. **Running the Script**  
   You can run the ACO algorithm by executing the `ACO_main_script.py` file. Open a terminal, navigate to the project directory, and run:

   ```bash
   python ACO_main_script.py
   ```

4. **Configuration Parameters**  
   In `ACO_main_script.py`, several parameters can be adjusted:

   - `ants_num`: Number of ants in each iteration.
   - `max_iter`: Maximum number of iterations.
   - `beta`, `q0`, `alpha`: Parameters influencing the ACO algorithm's behavior and convergence.

5. **Results and Visualization**  
   After running the script, results are saved in a specified results directory. The program may also generate visualizations of the best solution found by the ants, which you can view or save.

## File-Specific Details

- **`ant.py`**: Implements the logic for an individual ant’s journey, including path selection, constraint handling, and cost calculation.
- **`basic_aco.py`**: Manages the entire ACO process, from initializing the ants and pheromone trails to handling iteration-based updates.
- **`vprtw_aco_figure.py`**: Uses matplotlib to plot the VRPTW solution, showing nodes and routes.
- **`vrptw_base.py`**: Contains helper classes, including `Node` for customer locations and `VrptwGraph` to represent the problem graph.

## Example

Ensure `ACO_main_script.py` has the correct path to your VRPTW data file, then execute:

```bash
python ACO_main_script.py
```

You should see progress updates in the terminal, and the results, including route cost and solution paths, will be output to the specified files or directories.
