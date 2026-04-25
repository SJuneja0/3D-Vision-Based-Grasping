import gymnasium as gym
import panda_gym
import time
import pybullet as pb
import os
import numpy as np
import cv2
from tqdm import tqdm
from PIL import Image

env = gym.make('PandaReach-v3', render_mode="human")
env = env.unwrapped

## GETS PYBULLET INFORMATION
sim = env.sim
pb_client = sim.physics_client
robot_id = env.sim._bodies_idx["panda"]
EE_INDEX = 8 # panda_hand

## GETS LINK STATE OF END EFFECTOR
linkstate = pb_client.getLinkState(robot_id, EE_INDEX)


# ## FIND GOOD LINK INDEX FOR END EFFECTOR
# num_joints = pb_client.getNumJoints(robot_id)

# # printing off the joint indexes
# for i in range(num_joints):
#     info = pb_client.getJointInfo(robot_id, i)
#     print(i, info[12].decode("utf-8"))



SAVE_DIR = "test/data/scene_1" # image save directory
IMG_W, IMG_H = 256, 256
FOV = 60 # Field of View
NEAR, FAR = .08, 5.0 # Closest and farthest visible distance

os.makedirs(f"{SAVE_DIR}/images", exist_ok=True)

link_state = pb_client.getLinkState(robot_id, 8, computeForwardKinematics=True)


def render_image(pos, quat):

    rot = np.array(pb.getMatrixFromQuaternion(quat)).reshape(3, 3)

    # PyBullet camera looks along +Z
    forward = rot @ np.array([0, 0, 1])
    up = rot @ np.array([0, -1, 0])

    target = pos + 0.1 * forward
    print("Forward: ", forward)
    print("Target: ", target)

    view = pb_client.computeViewMatrix(pos, target, up)
    proj = pb_client.computeProjectionMatrixFOV(
        fov=FOV,
        aspect=IMG_W / IMG_H,
        nearVal=NEAR,
        farVal=FAR
    )

    _, _, rgb, depth, _ = pb_client.getCameraImage(
        width=IMG_W,
        height=IMG_H,
        viewMatrix=view,
        projectionMatrix=proj
    )

    rgb = np.reshape(rgb, (IMG_H, IMG_W, 4))[:, :, :3]
    return rgb, depth

hand_pos = link_state[0]
hand_quat = link_state[1]
rgb, depth = render_image(hand_pos, hand_quat)
print(rgb.shape)

img_path = f"test/data/scene_2/images/data_near_07.png"
Image.fromarray(rgb).save(img_path)



# For each episode, perform an action
for _ in tqdm(range(1000), desc="Episode"):
    action = env.action_space.sample() # random action
    observation, reward, terminated, truncated, info = env.step(action)
    time.sleep(0.01)

    link_state = pb_client.getLinkState(robot_id, 8, computeForwardKinematics=True)
    hand_pos = link_state[0]
    hand_quat = link_state[1]
    rgb, depth = render_image(hand_pos, hand_quat)
    cv2.imshow("Test Image", rgb)
    cv2.waitKey()

    if terminated or truncated:
        observation, info = env.reset()