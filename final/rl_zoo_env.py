from panda_gym.envs.core import RobotTaskEnv
from panda_gym.pybullet import PyBullet
from panda_gym.envs.robots.panda import Panda
from gymnasium import spaces
from typing import Dict

from rl_zoo_task import FinalPickAndPlace
import numpy as np
import time
from reconstruct import reconstruct
from camera import camera


class FinalEnv(RobotTaskEnv):
    """My robot-task environment."""

    def __init__(self, render_mode="rgb_array", urdf="002_master_chef_can.urdf"):
        
        self.sim = PyBullet(render_mode=render_mode)
        self.robot = Panda(self.sim, base_position=np.array([-0.5, 0, 0]))
        self.task = FinalPickAndPlace(self.sim, urdf) 
        self.recon = reconstruct()
        self.cam = camera(pb_client=self.sim.physics_client)
        self.pc = np.zeros((1024, 3), dtype=np.float32)
        
        super().__init__(self.robot, self.task)
        time.sleep(1)
        # Overrride observation space
        self.observation_space = spaces.Dict(
            dict(
                observation=spaces.Box(-10.0, 10.0, shape=(19,), dtype=np.float32),
                desired_goal=spaces.Box(-10.0, 10.0, shape=(3,), dtype=np.float32),
                achieved_goal=spaces.Box(-10.0, 10.0, shape=(3,), dtype=np.float32),
                valid_pc=spaces.Box(0.0, 1.0, shape=(1,), dtype=np.float32),
                point_cloud=spaces.Box(-1.0, 1.0, shape=(1024, 3), dtype=np.float32),
            )
        )
        

    def _get_obs(self) -> Dict[str, np.ndarray]:
        robot_obs = self.robot.get_obs().astype(np.float32)  # robot state
        task_obs = self.task.get_obs().astype(np.float32)  # object position, velocity, etc...
        observation = np.concatenate([robot_obs, task_obs])
        achieved_goal = self.task.get_achieved_goal().astype(np.float32)
        if (self.pc == np.zeros((1024, 3), dtype=np.float32)).all():
            self.pc = self.get_pointcloud()
            vpc = np.array([0])
        else:
            vpc = np.array([1])
        return {
            "observation": observation,
            "achieved_goal": achieved_goal,
            "desired_goal": self.task.get_goal().astype(np.float32),
            "point_cloud": self.pc.astype(np.float32),
            "valid_pc": vpc.astype(np.float32),
        }
    
    def get_pointcloud(self):
        rgb, depth, seg, pos, quat = self.cam.renderEE(robot_id=self.sim._bodies_idx["panda"])
        object_id = self.sim._bodies_idx["object"]
        mask = seg == object_id
        depth[~mask] = 0
        rgb[~mask] = 0

        intrinsic = self.cam.compute_intrinsics()
        pc = self.recon.create_pointcloud(rgb, depth, intrinsic)

        cpc = self.recon.clean_global_pc(pc)
        return cpc


if __name__ == "__main__": 
    from stable_baselines3.common.env_checker import check_env
    env = FinalEnv(render_mode="human", urdf="003_cracker_box.urdf")

    print("-----------Checking-----------")
    check_env(env)
    env.close()
    print("---terminated sucsessfully---")
