import gymnasium as gym
import panda_gym
import time

env = gym.make("PandaReach-v3", render_mode="human")
observation, info = env.reset()

# Action demo
for _ in range(1000):
    current_position = observation["observation"][0:3]
    desired_position = observation["desired_goal"][0:3]
    action = 5.0 * (desired_position - current_position)
    observation, reward, terminated, truncated, info = env.step(action)
    time.sleep(0.01)
    if terminated or truncated:
        observation, info = env.reset()

env.close()