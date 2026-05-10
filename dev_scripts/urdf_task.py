from panda_gym.envs.tasks.pick_and_place import PickAndPlace
import numpy as np

class URDFTask(PickAndPlace):
    def __init__(self, sim, urdf):
        self.sim = sim
        self.urdf = urdf
        self.sim.physics_client.setAdditionalSearchPath("data/object2urdf/examples/ycb_assets/")
        self.object_size = 0.05
        super().__init__(sim)

    def _create_scene(self) -> None:
        """Create the scene."""
        # self.sim.create_plane(z_offset=-0.4)
        # self.sim.create_table(length=1.1, width=0.7, height=0.4, x_offset=-0.3)

        self.object_id = self.sim.loadURDF(
            body_name="object",
            fileName=self.urdf,
            basePosition=[0.5, 0, 0.1],
        )

        self.sim.create_plane(z_offset=-0.4)
        self.sim.create_table(length=1.1, width=0.7, height=0.4, x_offset=-0.3)
        self.sim.create_box(
            body_name="target",
            half_extents=np.ones(3) * self.object_size / 2,
            mass=0.0,
            ghost=True,
            position=np.array([0.0, 0.0, 0.05]),
            rgba_color=np.array([0.1, 0.9, 0.1, 0.3]),
        )

    # Function is used to control obj position after reset (USE THIS)
    def _sample_object(self) -> np.ndarray:
        """Randomize start position of object."""
        object_position = np.array([0.65, 0.0, -0.05])
        # noise = self.np_random.uniform(self.obj_range_low, self.obj_range_high)
        # object_position += noise
        print("object position: ", object_position)
        return object_position

    def disp_pos(self, env):
        pos, orn = self.sim.physics_client.getBasePositionAndOrientation(env.sim._bodies_idx["object"])
        vel = self.sim.physics_client.getBaseVelocity(env.sim._bodies_idx["object"])
        print("actual pos:", pos)
        print("actual vel: ", vel)
        self.sim.physics_client.addUserDebugLine([0,0,0], [1,0,0], [1,0,0])

