import gymnasium as gym
import panda_gym
import time
import pybullet as pb
import os
import numpy as np
import cv2
from tqdm import tqdm
from PIL import Image

class camera():
    def __init__(self, pb_client, fov=60, image_width=256, image_height=256, render_near=0.08, render_far=3.0):
        self.pb_client = pb_client
        self.fov = fov
        self.image_width = image_width
        self.image_height = image_height
        self.render_near = render_near
        self.render_far = render_far

    def renderEE(self, robot_id, EE_idx, computeFK=True):
        link_state = self.pb_client.getLinkState(robot_id, EE_idx, computeForwardKinematics=computeFK)

        pos = link_state[0]
        quat = link_state[1]

        # Find camera Z+ axis orientation
        rot = np.array(pb.getMatrixFromQuaternion(quat)).reshape(3, 3)
        forward = rot @ np.array([0, 0, 1]) # Projected Z axis
        up = rot @ np.array([0, -1, 0]) # Projected -Y axis

        target = pos + 0.1 * forward # Camera position

        view = self.pb_client.computeViewMatrix(pos, target, up)
        proj = self.pb_client.computeProjectionMatrixFOV(
            fov=self.fov,
            aspect=self.image_width / self.image_height,
            nearVal=self.render_near,
            farVal=self.render_far
        )

        _, _, rgb, depth, _ = self.pb_client.getCameraImage(
            width=self.image_width,
            height=self.image_height,
            viewMatrix=view,
            projectionMatrix=proj
        )

        rgb = np.reshape(rgb, (self.image_height, self.image_width, 4))[:, :, :3]
        return rgb, depth, pos, quat
    

    def renderPosQuat(self, pos, quat):

        # Find camera Z+ axis orientation
        rot = np.array(pb.getMatrixFromQuaternion(quat)).reshape(3, 3)
        forward = rot @ np.array([0, 0, 1]) # Projected Z axis
        up = rot @ np.array([0, -1, 0]) # Projected -Y axis

        target = pos + 0.1 * forward # Camera position

        view = self.pb_client.computeViewMatrix(pos, target, up)
        proj = self.pb_client.computeProjectionMatrixFOV(
            fov=self.FOV,
            aspect=self.image_width / self.image_height,
            nearVal=self.render_near,
            farVal=self.render_far
        )

        _, _, rgb, depth, _ = self.pb_client.getCameraImage(
            width=self.image_width,
            height=self.image_height,
            viewMatrix=view,
            projectionMatrix=proj
        )

        rgb = np.reshape(rgb, (self.image_height, self.image_width, 4))[:, :, :3]
        return rgb, depth

