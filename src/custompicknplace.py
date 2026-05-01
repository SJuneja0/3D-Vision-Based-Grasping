from panda_gym.envs.tasks.pick_and_place import PickAndPlace
import numpy as np

class MyPickAndPlace(PickAndPlace):
    def __init__(self, sim):
        self.sim = sim
        # self.sim.physics_client.setAdditionalSearchPath("test/assets/")
        self.sim.physics_client.setAdditionalSearchPath("data/object2urdf/examples/ycb_assets/")
        self.object_size = 0.05
        super().__init__(sim)

    ## Testing adding an object using parent's _create_scene()
    # def _create_scene(self):
    #     super()._create_scene()

    #     self.sim.physics_client.setAdditionalSearchPath("test/assets/")

    #     self.object_id = self.sim.loadURDF(
    #         body_name="object",
    #         fileName="soccerball.urdf",
    #         basePosition=[0.5, 0, 0.02]
    #     )

    def _create_scene(self) -> None:
        """Create the scene."""
        self.sim.create_plane(z_offset=-0.4)
        self.sim.create_table(length=1.1, width=0.7, height=0.4, x_offset=-0.3)

        self.object_id = self.sim.loadURDF(
            body_name="object",
            fileName="006_mustard_bottle.urdf",
            # fileName="002_master_chef_can.urdf",
            # fileName="soccerball.urdf",
            basePosition=[0.5, 0, 0.1],
            # useFixedBase=False
        )

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
        object_position = np.array([0.7, 0.0, self.object_size / 2])
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

