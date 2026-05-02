import numpy as np
import open3d as o3d

class reconstruct():
    def __init__(self):
        pass


    def create_pointcloud(self, rgb, depth, intrinsic_param):
        intrinsic = o3d.camera.PinholeCameraIntrinsic(
            intrinsic_param["width"],
            intrinsic_param["height"],
            intrinsic_param["fx"],
            intrinsic_param["fy"],
            intrinsic_param["cx"],
            intrinsic_param["cy"]
            )
        
        rgb_o3d = o3d.geometry.Image(rgb.astype(np.uint8))
        depth_o3d = o3d.geometry.Image(depth.astype(np.float32))

        rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
            color=rgb_o3d,
            depth=depth_o3d,
            depth_scale=1.0, # check params
            depth_trunc=2.0, # check params
            convert_rgb_to_intensity=False # check params
        )

        pc = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd, intrinsic)

        return pc
    
    def create_global_pointcloud(self, dataset):
        global_pc = o3d.geometry.PointCloud()

        for rgb, depth, intrinsic, camera_pose in dataset:
            pc = self.create_pointcloud(rgb, depth, intrinsic)
            pc.transform(camera_pose)

            global_pc += pc
        
        return global_pc
    
    # add default value maybe?
    def sample_global_pc(self, global_pc, voxel_size):
        return global_pc.voxel_down_sample(voxel_size=voxel_size)

    def clean_global_pc(self, global_pc, nb_neighbors=20, std_ratio=0.2, num_points=1024):
        # Remove Outliers
        global_pc, _ = global_pc.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)

        # Normalize points around a center and size
        global_points = np.asarray(global_pc.points)
        center = global_points.mean(axis=0)
        global_points -= center
        scale = np.max(np.linalg.norm(global_points, axis=1))
        global_points /= scale

        # Fix the number of points for training a NN (Fixed input size)
        if len(global_points) > num_points:
            idx = np.random.choice(len(global_points), num_points, replace=False)
        else:
            idx = np.random.choice(len(global_points), num_points, replace=True)

        global_points = global_points[idx]

    def viz_pc(self, pc):
        o3d.visualization.draw_geometries([pc])