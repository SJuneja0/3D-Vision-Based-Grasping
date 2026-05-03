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
import time
from policy import Policy
import torch

class train():
    def __init__(self, episodes=1, time_steps=500):
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
            rgb, depth, seg, pos, quat = self.cam.renderEE(robot_id=self.env.sim._bodies_idx["panda"])
            Image.fromarray(rgb).save(img_path)
            return rgb, depth, seg, pos, quat
    
    def change_env(self, urdf):
        self.env.close()
        self.env = FinalEnv(render_mode="human", urdf=urdf)
        self.cam = camera(pb_client=self.env.sim.physics_client)

    def move_in_frame(self, observation, z_offset=0.3): # moves the robot to start above the obj
        obj_pose = observation["achieved_goal"][0:3]
        robot_pose = observation["observation"][0:3]
        xy_action = obj_pose[0:2] - robot_pose[0:2]
        z_action = obj_pose[2] + z_offset - robot_pose[2]

        term = False
        if abs(np.sum(xy_action) + z_action) < 0.001:
            term = True
        
        action = np.array(np.append(np.append(xy_action, z_action), 0))
        if np.linalg.norm(action) < 0.1:
            action /= np.linalg.norm(action)
            action *= 0.1
        return action, term



if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="This is a test")
    parser.add_argument("--agent", help="The agent")
    args = parser.parse_args()
    print(args.test)

    trainer = train(episodes=1)
    list_urdf = listURDF().list_URDF()
    num_urdf = len(list_urdf)

    # Torch values
    model = Policy()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    
    for i in range(trainer.episodes):
        # Initiate env with random object
        rand_urdf = list_urdf[random.randint(0, num_urdf-1)]
        trainer.init_env(rand_urdf) if trainer.env is None else trainer.change_env(rand_urdf)
        observation, info = trainer.env.reset()


        # Move robot above obj and collect images
        images_info = []
        term = False
        while not term:
            action, term = trainer.move_in_frame(observation)
            observation, reward, terminated, truncated, info = trainer.env.step(action) # TODO: Improve this thing's precision
        print("Reached Top: Init Recon")
        time.sleep(0.5)
        
        # Take pic from top
        recon = reconstruct()
        img_path = f"final/images/test_{i}.jpg"
        rgb, depth, seg, pos, quat = trainer.take_pic(img_path) 

        # Mask out only the obj
        object_id = trainer.env.sim._bodies_idx["object"]
        mask = seg == object_id
        depth[~mask] = 0
        rgb[~mask] = 0

        # create the point cloud
        intrinsic = trainer.cam.compute_intrinsics()
        pc = recon.create_pointcloud(rgb, depth, intrinsic)
        # recon.viz_pc(pc)

        # clean the pointcloud for the NN
        # including making it 1024 points
        cpc = recon.clean_global_pc(pc)

        # recon.viz_pc(recon.numpy_to_pc(cpc)) 

        # # potentially add additional pictures here from other angles to make a better picture

        print("OBSERVATION: ", observation)
        print("POINT CLOUD: ", cpc)
        print("PC SHAPE: ", cpc.shape)

        done = False
        j = 0
        while not done and j < trainer.time_steps:
            obs = observation["observation"]
            ag = observation["achieved_goal"]
            dg = observation["desired_goal"]
            input_obs = np.concat((obs, ag, dg))

            input = {"pc": cpc, "observation" : input_obs}

            cpc = torch.tensor(cpc, dtype=torch.float32).unsqueeze(0)
            input_obs = torch.tensor(input_obs, dtype=torch.float32).unsqueeze(0)

            action = model(pc=cpc, observation=input_obs)
            observation, reward, terminated, truncated, info = trainer.env.step(action.detach().numpy()[0])

            reward = torch.tensor(reward, dtype=torch.float32)
            # log_prob = model.log_prob(action)
            # loss = -(log_prob * reward)
            loss = -reward
            

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            done = terminated


    print("-----Terminating Env-----")
    trainer.env.close()








# Notes:
# while not term:
#     action, term = trainer.move_in_frame(observation)
#     observation, reward, terminated, truncated, info = trainer.env.step(action * 3)
#     # img_path = f"final/images/test_{i}.jpg"
#     # rgb, depth, seg, pos, quat = trainer.take_pic(img_path) 
#     # images_info.append( (rgb, depth, pos, quat) )
# time.sleep(0.5)


# dataset = []
# for (rgb, depth, pos, quat) in images_info:
#     intrinsic = trainer.cam.compute_intrinsics()
#     # camera_pose = trainer.cam.compute_xform(pos, quat)
#     camera_pose = trainer.cam.compute_xform(pos, quat)
#     dataset.append( (rgb, depth, intrinsic, camera_pose) )
# recon = reconstruct()

# ## TODO: TEST
# i = 0
# for (rgb, depth, intrinsic, camera_pose) in dataset:
#     pc = recon.create_pointcloud(rgb, depth, intrinsic)
# global_pc = recon.create_global_pointcloud(dataset)
# recon.viz_pc(global_pc)
# trimmed_global_pc = recon.clean_global_pc(global_pc=global_pc)
# recon.viz_pc(trimmed_global_pc)

# for j in range(trainer.time_steps):