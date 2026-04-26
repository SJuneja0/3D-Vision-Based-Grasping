from panda_gym.envs.core import RobotTaskEnv
from panda_gym.pybullet import PyBullet
from panda_gym.envs.robots.panda import Panda

from customtask import MyTask
from custompicknplace import MyPickAndPlace


class MyRobotTaskEnv(RobotTaskEnv):
    """My robot-task environment."""

    def __init__(self, render_mode):
        self.sim = PyBullet(render_mode=render_mode)
        self.robot = Panda(self.sim)
        # task = MyTask(sim)
        self.task = MyPickAndPlace(self.sim)
        

        super().__init__(self.robot, self.task)


if __name__ == "__main__": 
    import time
    from camera import camera
    from PIL import Image

    env = MyRobotTaskEnv(render_mode="human")

    cam = camera(pb_client=env.sim.physics_client)
    rgb, _, _, _ = cam.renderEE(robot_id=env.sim._bodies_idx["panda"])
    img_path = f"src/cam_test.png"
    Image.fromarray(rgb).save(img_path)

    env.task.disp_pos(env)
    time.sleep(2)
    print("RESETING")
    

    for i in range(4):
        # action = env.action_space.sample() # random action
        action = [0, 0, 0, 0]
        # observation, reward, terminated, truncated, info = env.step(action)
        print(i)
        observation, info = env.reset()
        env.task.disp_pos(env)
        time.sleep(2)
        

        # if terminated or truncated:
        #     observation, info = env.reset()
    
    print("---terminated sucsessfully---")