from panda_gym.envs.core import RobotTaskEnv
from panda_gym.pybullet import PyBullet
from panda_gym.envs.robots.panda import Panda

from final_task import FinalPickAndPlace
import numpy as np
import time


class FinalEnv(RobotTaskEnv):
    """My robot-task environment."""

    def __init__(self, render_mode, urdf):
        self.sim = PyBullet(render_mode=render_mode)
        # self.robot = Panda(self.sim, base_position=np.array([0, 0, 0])) #TODO: Change this val later
        self.robot = Panda(self.sim)
        self.task = FinalPickAndPlace(self.sim, urdf)        

        super().__init__(self.robot, self.task)


if __name__ == "__main__": 
    import time
    from camera import camera
    from PIL import Image

    env = FinalEnv(render_mode="human")

    cam = camera(pb_client=env.sim.physics_client)
    rgb, _, _, _ = cam.renderEE(robot_id=env.sim._bodies_idx["panda"])
    img_path = f"final/cam_test.png"
    Image.fromarray(rgb).save(img_path)
    
    observation, info = env.reset()

    first_pos = observation["observation"][0:2]
    print("First Pose: ", first_pos)
    for i in range(500):
        print("i: ", i)
        obj_pos = observation["achieved_goal"][0:2]
        # print(obj_pos)
        robot_pos = observation["observation"][0:2]
        print("Robot Pose: ", robot_pos)
        if not (robot_pos == first_pos).all():
            print("ROBOT MOVED")
        
        action = obj_pos - robot_pos
        print(action)
        if np.sum(action) < 0.2:
            print("REACHED GOAL")
        time.sleep(0.01)
        observation, reward, terminated, truncated, info = env.step(np.append(np.append(action, 0), 0))
        

        # if terminated or truncated:
        #     observation, info = env.reset()
    
    print("---terminated sucsessfully---")