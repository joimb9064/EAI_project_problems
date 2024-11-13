
# Particle Swarm Optimization (PSO)

This repository contains a set of Python modules designed for constraint-based decoding, optimization, and evaluation of route scheduling solutions, especially applicable to vehicle routing problems. The project employs Particle Swarm Optimization and techniques to ensure that generated routes meet constraints such as time windows, capacity limits, and service requirements.

## Project Structure

- **`constraintBasedDecoder.py`**: Implements decoding functions that enforce specific constraints on solutions, transforming encoded representations into usable formats for evaluation or optimization.
  
- **`decodeInstance.py`**: Contains functions to decode individual instances, applying detailed constraints to each specific route.

- **`evaluate.py`**: Provides evaluation methods to assess the overall quality of solutions, calculating scores based on distance, time, or unmet demands.

- **`evaluateInstance.py`**: Contains methods to evaluate individual route instances within the larger solution, enabling focused assessments and debugging of specific routes.

- **`initializePopulation.py`**: Initializes the population of routes or solutions, essential for evolutionary and population-based optimization algorithms.

- **`plotTools.py`**: Visualizes customer locations, routes, and vehicle paths. It includes functions to display customer data and plot the paths taken by optimized solutions.

- **`update.py`**: Houses helper functions to update positions, velocities, and constraints, which are integral to the optimization process.

## Getting Started

### Prerequisites

- Python 3.x
- `numpy`
- `matplotlib`

Install the dependencies with:
```bash
pip install -r requirements.txt
```

### Running the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/route-optimization.git
   cd route-optimization
   ```

2. Execute specific modules or integrate them into a main script as needed. For example, to evaluate a solution, you can use:
   ```python
   from evaluate import evaluateParticle
   # Code to define a solution and evaluate it
   ```

3. To visualize the optimized routes and customer distribution, use the `plotTools.py` functions:
   ```python
   from plotTools import plotCustomers, plotParticle
   ```

### Example Usage

```python
from initializePopulation import initializePopulation
from evaluate import evaluateParticle
from plotTools import plotCustomers, plotParticle

# Initialize a population of solutions
population = initializePopulation(...)

# Evaluate a particle
numberOfVehicles, totalDistance = evaluateParticle(population[0], distances, depotIndex)

# Plot customers and optimized paths
plotCustomers(xCoord, yCoord, demand, readyTime, dueDate, service, arrivalTimeListBest, capacityListBest, numberOfCustomers)
plotParticle(xCoord, yCoord, particlePosition)
```

### Function Overview

Each module contains functions that contribute to constraint-based decoding and optimization:

- **`constraintBasedDecoder.py`**
  - `decodeSolution`: Decodes an entire solution to ensure it meets set constraints.

- **`decodeInstance.py`**
  - `decodeIndividualInstance`: Decodes and validates a single route instance within a larger solution.

- **`evaluate.py`**
  - `evaluateParticle`: Evaluates a particle's position, calculating the number of vehicles used and the total distance traveled.
  - `objective`: Computes the objective cost based on selected modes like minNV (minimize number of vehicles) or minDist (minimize distance).
  - `updateBest`: Updates the best known positions and costs if the current solution is better than the previous best.

- **`initializePopulation.py`**
  - `initializePopulation`: Creates an initial set of possible solutions.
  - `velocity`: Defines velocity for optimization particles.

- **`plotTools.py`**
  - `plotCustomers`: Plots customer locations and details.
  - `plotParticle`: Visualizes the path taken by a specific particle.

- **`update.py`**
  - `coeffTimesVelocity`, `addVelocities`, `subtractPositions`, etc.: Helper functions for managing velocity and position updates in the optimization process.
  - `localSearch`: Attempts local improvements on solutions.


