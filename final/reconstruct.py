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
        global_pcd = o3d.geometry.PointCloud()

        for rgb, depth, intrinsic, camera_pose in dataset:
            pc = self.create_pointcloud(rgb, depth, intrinsic)
            pc.transform(camera_pose)

            global_pc += pc
        
        return global_pc
    
    # add default value maybe?
    def sample_gpc(self, gpc, voxel_size):
        return gpc.voxel_down_sample(voxel_size=voxel_size)

    def remove_outliers(self, gpc, nb_neighbors, std_ratio):
        gpc, _ = gpc.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
        return gpc