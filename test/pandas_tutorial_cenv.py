from panda_gym.envs.core import RobotTaskEnv
from panda_gym.pybullet import PyBullet
from panda_gym.envs.robots.panda import Panda

from pandas_tutorial_ctask import MyTask


class MyRobotTaskEnv(RobotTaskEnv):
    """My robot-task environment."""

    def __init__(self, render_mode):
        sim = PyBullet(render_mode=render_mode)
        robot = Panda(sim)
        task = MyTask(sim)
        super().__init__(robot, task)


if __name__ == "__main__": 
    env = MyRobotTaskEnv(render_mode="human")

    observation, info = env.reset()

    for _ in range(1000):
        action = env.action_space.sample() # random action
        observation, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            observation, info = env.reset()
    
    print("---terminated sucsessfully---")