# Create an env that can
# 1. Collect images
# 2. Load different urdfs
# 3. Has a modular spot to accept actions
# 4. Can modularly create different episode lengths / params
from final_env import FinalEnv
from final_task import FinalPickAndPlace
from camera import camera
from PIL import Image


if __name__ == "__main__": 
    env = FinalEnv(render_mode="human")

    cam = camera(pb_client=env.sim.physics_client)
    rgb, _, _, _ = cam.renderEE(robot_id=env.sim._bodies_idx["panda"])
    img_path = f"final/cam_test.png"
    Image.fromarray(rgb).save(img_path)

