
# Q-Learning for Taxi Environment

This project implements the Q-learning algorithm for training an agent to navigate the Taxi-v3 environment, a classic reinforcement learning problem where a taxi must pick up and drop off passengers. The OpenAI Gym library provides the environment setup, and the Q-learning approach allows the agent to learn through trial and error.

## Requirements

Ensure the following libraries are installed:

- `gym`
- `numpy`
- `matplotlib`
- `torch` (for potential use in other models)

Install dependencies using:
```bash
pip install gym numpy matplotlib torch
```

Additionally, if running in a Jupyter or Colab notebook, install:
```bash
apt-get install xvfb python-opengl ffmpeg
pip install pyvirtualdisplay
```

## Project Structure

1. **Environment Setup**  
   - The Taxi-v3 environment is initialized using `gym.make("Taxi-v3")`. This environment is a grid where the taxi must navigate to pick up and drop off passengers while avoiding obstacles.

2. **Random Policy Simulation**  
   - Before applying Q-learning, the notebook includes a section that simulates the taxi agent using a random policy to provide a baseline for performance comparison.

3. **Q-Learning Implementation**  
   - The Q-learning algorithm is implemented to update the agent's knowledge (Q-values) based on rewards received. Parameters include:
     - **Learning Rate (α)**: Controls how quickly the Q-values update.
     - **Discount Factor (γ)**: Balances immediate and future rewards.
     - **Exploration Rate (ε)**: Determines the exploration-exploitation tradeoff.

4. **Training the Agent**  
   - The notebook runs the Q-learning algorithm over multiple episodes, gradually refining the agent’s ability to reach goals more efficiently.

5. **Visualization and Results**  
   - Training results, including rewards and policy improvement, are visualized to show the agent’s progress over time.

## Usage Instructions

1. **Open the Notebook**  
   Load the notebook (`Q_Learning_Taxi_V3.ipynb`) in Jupyter Notebook, Jupyter Lab, or Google Colab.

2. **Execute Cells Sequentially**  
   Run each cell in order to set up the environment, simulate the random policy, and then train the agent using Q-learning.

3. **Adjust Hyperparameters**  
   Modify parameters in the Q-learning section to experiment with learning rates, discount factors, and exploration rates.

4. **Observe Results**  
   View the training results and reward visualizations to assess the agent’s performance.

## Example Execution

Ensure all dependencies are installed, then start from the top of the notebook. After running the setup cells, observe the agent’s learning progress as it completes more successful pickups and drop-offs with fewer mistakes.

