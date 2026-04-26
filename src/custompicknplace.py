from panda_gym.envs.tasks.pick_and_place import PickAndPlace
import numpy as np

class MyPickAndPlace(PickAndPlace):
    def __init__(self, sim):
        self.sim = sim
        self.sim.physics_client.setAdditionalSearchPath("test/assets/")
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
            fileName="soccerball.urdf",
            basePosition=[0.5, 0, 0.02]
        )

        self.sim.create_sphere(
            body_name="target",
            radius=0.02,
            mass=0.0,
            ghost=True,
            position=np.zeros(3),
            rgba_color=np.array([0.1, 0.9, 0.1, 0.3]),
        )

        # self.sim.create_box(
        #     body_name="object",
        #     half_extents=np.ones(3) * self.object_size / 2,
        #     mass=1.0,
        #     position=np.array([0.0, 0.0, self.object_size / 2]),
        #     rgba_color=np.array([0.1, 0.9, 0.1, 1.0]),
        # )
        # self.sim.create_box(
        #     body_name="target",
        #     half_extents=np.ones(3) * self.object_size / 2,
        #     mass=0.0,
        #     ghost=True,
        #     position=np.array([0.0, 0.0, 0.05]),
        #     rgba_color=np.array([0.1, 0.9, 0.1, 0.3]),
        # )

