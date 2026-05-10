import os
import numpy as np
import pybullet as p
import pybullet_data
import time

# Set constants
SAVE_DIR = "test/data/scene_1" # image save directory
IMG_W, IMG_H = 128, 128
FOV = 60 # Field of View
NEAR, FAR = 0.01, 2.0 # Closest and farthest visible distance

os.makedirs(f"{SAVE_DIR}/images", exist_ok=True)

# =========================
# INIT SIM
# =========================
p.connect(p.GUI)  # p.DIRECT = no window, for faster execution
p.setAdditionalSearchPath(pybullet_data.getDataPath()) # finds build-in assets
p.setGravity(0, 0, -9.8)

# Load ground
plane = p.loadURDF("plane.urdf") 

# Load Panda robot
robot = p.loadURDF("franka_panda/panda.urdf", useFixedBase=True)

# Simple object (obj and position)
cube = p.loadURDF("cube_small.urdf", [0.5, 0, 0.02])

# Panda end-effector index
EE_INDEX = 11

# =========================
# CAMERA FUNCTIONS
# =========================
def get_camera_matrices(pos, quat):
    rot = np.array(p.getMatrixFromQuaternion(quat)).reshape(3, 3)

    # PyBullet camera looks along +Z
    forward = rot @ np.array([0, 0, 1])
    up = rot @ np.array([0, -1, 0])

    target = pos + 0.1 * forward

    view = p.computeViewMatrix(pos, target, up)
    proj = p.computeProjectionMatrixFOV(
        fov=FOV,
        aspect=IMG_W / IMG_H,
        nearVal=NEAR,
        farVal=FAR
    )
    return view, proj

def render_camera(view, proj):
    _, _, rgb, depth, _ = p.getCameraImage(
        width=IMG_W,
        height=IMG_H,
        viewMatrix=view,
        projectionMatrix=proj
    )

    rgb = np.reshape(rgb, (IMG_H, IMG_W, 4))[:, :, :3]
    return rgb, depth

# =========================
# SAVE HELPERS
# =========================
pose_file = open(f"{SAVE_DIR}/poses.txt", "w")

def save_pose(idx, pos, quat):
    q = quat
    t = pos
    pose_file.write(
        f"{idx} {q[0]} {q[1]} {q[2]} {q[3]} {t[0]} {t[1]} {t[2]}\n"
    )

# =========================
# SIMPLE ROBOT MOTION
# =========================
def move_robot(step):
    # simple oscillation for demo
    joint_positions = [0.5 * np.sin(0.01 * step)] * 7
    for i in range(7):
        p.setJointMotorControl2(
            robot, i,
            p.POSITION_CONTROL,
            targetPosition=joint_positions[i]
        )

# =========================
# MAIN LOOP
# =========================
num_frames = 200

for i in range(num_frames):
    move_robot(i)
    p.stepSimulation()

    # Get EE pose
    link_state = p.getLinkState(robot, EE_INDEX)
    pos = link_state[0]
    quat = link_state[1]

    # Camera matrices
    view, proj = get_camera_matrices(pos, quat)

    # Render
    rgb, depth = render_camera(view, proj)

    # Save image
    img_path = f"{SAVE_DIR}/images/{i:04d}.png"
    from PIL import Image
    Image.fromarray(rgb).save(img_path)

    # Save pose
    save_pose(i, pos, quat)

    time.sleep(1./240.)

pose_file.close()
p.disconnect()