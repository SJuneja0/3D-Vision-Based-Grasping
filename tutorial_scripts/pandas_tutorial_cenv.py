from panda_gym.envs.core import RobotTaskEnv
from panda_gym.pybullet import PyBullet
from panda_gym.envs.robots.panda import Panda

# from custom_task_test import MyTask
# from pandas_tutorial_ctask import MyTask
from task_searchpath_test import MyTask


class MyRobotTaskEnv(RobotTaskEnv):
    """My robot-task environment."""

    def __init__(self, render_mode):
        sim = PyBullet(render_mode=render_mode)
        robot = Panda(sim)
        task = MyTask(sim)
        super().__init__(robot, task)


if __name__ == "__main__": 
    import time
    env = MyRobotTaskEnv(render_mode="human")

    observation, info = env.reset()

    for _ in range(1000):
        # action = env.action_space.sample() # random action
        action = [0, 0, 0, 0]
        observation, reward, terminated, truncated, info = env.step(action)
        
        time.sleep(0.01)

        env.reset()

        if terminated or truncated:
            observation, info = env.reset()
    
    print("---terminated sucsessfully---")