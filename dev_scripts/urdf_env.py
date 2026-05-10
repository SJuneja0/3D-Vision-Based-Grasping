from panda_gym.envs.core import RobotTaskEnv
from panda_gym.pybullet import PyBullet
from panda_gym.envs.robots.panda import Panda

from urdf_task import URDFTask


class URDFEnv(RobotTaskEnv):
    """My robot-task environment."""

    def __init__(self, render_mode, urdf):
        self.sim = PyBullet(render_mode=render_mode)
        self.robot = Panda(self.sim)
        # task = MyTask(sim)
        self.task = URDFTask(self.sim, urdf)

        super().__init__(self.robot, self.task)


if __name__ == "__main__": 
    import time
    from camera import camera
    from PIL import Image

    # list_urdf = ["002_master_chef_can.urdf", "006_mustard_bottle.urdf"]
    from list_urdf import listURDF
    
    list_urdf = listURDF().list_URDF()

    for urdf in list_urdf:
        # Set up env
        env = URDFEnv("human", urdf)
        pb_client=env.sim.physics_client

        # Set up cam and take picture
        cam = camera(pb_client=pb_client)
        rgb, depth, seg, pos, quat = cam.renderEE(robot_id=env.sim._bodies_idx["panda"])
        img_path = f"src/obj_images/{urdf[:-5]}.png"
        Image.fromarray(rgb).save(img_path)
        
        print("===========")
        print(urdf[:-5])
        print("===========")

        # Display object spatial info
        env.task.disp_pos(env)
        observation, info = env.reset()
        
        from pynput import keyboard

        print("Waiting for the 'Enter' key...")

        def on_press(key):
            if key == keyboard.Key.enter:
                return False # Stopping the listener

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

        print("RESETING")
        env.close()
