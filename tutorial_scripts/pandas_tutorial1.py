import gymnasium as gym
import panda_gym
import time

env = gym.make('PandaReach-v3', render_mode="human")

observation, info = env.reset()

# Env setup demo
for _ in range(1000):
    action = env.action_space.sample() # random action
    observation, reward, terminated, truncated, info = env.step(action)
    time.sleep(0.01)
    if terminated or truncated:
        observation, info = env.reset()