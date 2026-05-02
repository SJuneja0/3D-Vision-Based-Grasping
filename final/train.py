# Create an env that can
# 1. Collect images
# 2. Load different urdfs
# 3. Has a modular spot to accept actions
# 4. Can modularly create different episode lengths / params
from final_env import FinalEnv
from final_task import FinalPickAndPlace
from camera import camera
from PIL import Image
from list_urdf import listURDF
import argparse
import random
from reconstruct import reconstruct
import numpy as np

class train():
    def __init__(self, episodes=3, time_steps=500):
        self.env = None
        self.cam = None
        self.time_steps = time_steps
        self.episodes = episodes

    def init_env(self, urdf):
        self.env = FinalEnv(render_mode="human", urdf=urdf)
        self.cam = camera(pb_client=self.env.sim.physics_client)

    def take_pic(self, img_path=None):
            if img_path == None:
                print("NO VALID IMAGE PATH PASSED")
                return None
            rgb, depth, pos, quat = self.cam.renderEE(robot_id=self.env.sim._bodies_idx["panda"])
            Image.fromarray(rgb).save(img_path)
            return rgb, depth, pos, quat
    
    def change_env(self, urdf):
        self.env.close()
        self.env = FinalEnv(render_mode="human", urdf=urdf)
        self.cam = camera(pb_client=self.env.sim.physics_client)

    def move_in_frame(self, observation, z_offset=0.2): # moves the robot to start above the obj
        obj_pose = observation["achieved_goal"][0:3]
        robot_pose = observation["observation"][0:3]
        xy_action = obj_pose[0:2] - robot_pose[0:2]
        z_action = obj_pose[2] + z_offset - robot_pose[2]
        
        return np.array(np.append(np.append(robot_pose, z_action), 0))

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="This is a test")
    parser.add_arguement("--agent", help="The agent")
    args = parser.parse_args()
    print(args.test)

    trainer = train()
    list_urdf = args.agent.list_URDF()
    num_urdf = len(list_urdf)
    
    for i in range(trainer.episodes):
        # Initiate env with random object
        rand_urdf = list_urdf[random.randint(0, num_urdf-1)]
        trainer.init_env(rand_urdf) if trainer.env is None else trainer.change_env(rand_urdf)
        observation, info = trainer.env.reset()

        # Move robot above obj and collect images
        images_info = []
        term = False
        while not term:
            term = trainer.move_in_frame(observation)
            img_path = None
            rgb, depth, pos, quat = trainer.take_pic(img_path) 
            images_info.append( (rgb, depth, pos, quat) )


        # potentially add additional pictures here from other angles to make a better picture

        # Create a 3D representation of the object based on the photos
        # TODO: Need to remove background, can only have object in point cloud -> Color filterings?
        # Could also just take pics around the object and not make it relate to being eye-in-hand
        
        # TODO: Fill in None
        dataset = []
        for (rgb, depth, pos, quat) in images_info:
            intrinsic = trainer.cam.compute_intrinsics()
            camera_pose = trainer.cam.compute_xform(pos, quat)
            dataset.append( (rgb, depth, intrinsic, camera_pose) )
        recon = reconstruct()

        ## TEST
        for (rgb, depth, intrinsic, camera_pose) in dataset:
            pc = recon.create_pointcloud(rgb, depth, intrinsic)
            recon.viz_pc(pc)
        global_pc = recon.create_global_pointcloud(dataset)
        trimmed_global_pc = recon.clean_global_pc(global_pc=global_pc, nb_neighbors=None, std_ratio=None, num_points=None)
        recon.viz_pc(trimmed_global_pc)
        # ENDTEST

        for j in range(trainer.time_steps):

            action = None # TODO
            observation, reward, terminated, truncated, info = trainer.env.step(action)
            pass # TODO Finish the rest of the logic

