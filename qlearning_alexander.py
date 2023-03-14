import numpy as np

# Define the reward matrix for the Prisoner's Dilemma game
REWARD_MATRIX = np.array([[-1, -4], [0, -3]])
# Define the learning rate, discount factor, and exploration rate
LEARNING_RATE = 0.8
DISCOUNT_FACTOR = 0.95
EXPLORATION_RATE = 0.1

# Initialize the Q-table
Q_TABLE = np.zeros((2, 2))

# Define a function to select an action based on the current Q-values and the exploration rate
def select_action(state):
    if np.random.uniform() < EXPLORATION_RATE:
        # Explore by randomly choosing an action
        return np.random.choice([0, 1])
    else:
        # Exploit by choosing the action with the highest Q-value
        return np.argmax(Q_TABLE[state, :])

# Define the Q-learning algorithm
def q_learning(num_episodes):
    for i in range(num_episodes):
        # Reset the state to start a new episode
        state = np.random.choice([0, 1])
        while True:
            # Select an action based on the current state and Q-values
            action = select_action(state)
            
            # Execute the action and observe the next state and reward
            if action == 0:
                # Cooperate
                next_state = 0
                reward = REWARD_MATRIX[state, 0]
            else:
                # Defect
                next_state = 1
                reward = REWARD_MATRIX[state, 1]
            
            # Update the Q-value for the current state-action pair
            Q_TABLE[state, action] += LEARNING_RATE * (reward + DISCOUNT_FACTOR * np.max(Q_TABLE[next_state, :]) - Q_TABLE[state, action])
            
            # Transition to the next state
            state = next_state
            
            # Stop the episode if the game is over
            if state == 1:
                break
    
    # Return the learned Q-table
    return Q_TABLE

# Train the Q-learning algorithm for 1000 episodes
q_table = q_learning(10)

# Print the learned Q-values
print(q_table)
