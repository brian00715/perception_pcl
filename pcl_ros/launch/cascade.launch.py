from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    return LaunchDescription(
        [
            DeclareLaunchArgument("gui", default_value="true", description="Enable GUI"),
            DeclareLaunchArgument("test", default_value="true", description="Run tests"),
            DeclareLaunchArgument("leaf_size", default_value="0.05", description="Voxel grid leaf size"),
            # Node(
            #     package="pcl_ros",
            #     executable="filter_voxel_grid_node",
            #     name="filter_voxel_grid_node",
            #     parameters=[
            #         {
            #             "leaf_size": LaunchConfiguration("leaf_size"),
            #             "filter_field_name": "z",
            #             # "filter_limit_min": 0.4,
            #             # "filter_limit_max": 0.6,
            #             # "filter_limit_negative": False,
            #         }
            #     ],
            #     # remappings=[('input', '/camera/depth/color/points')]
            #     # remappings=[('input', 'points')]
            #     remappings=[("input", "/utlidar/cloud_deskewed"), ("output", "/pcl/voxel_grid")],
            # ),
            Node(
                package="pcl_ros",
                executable="filter_passthrough_node",
                name="passthrough",
                output="screen",
                parameters=[
                    {
                        "filter_field_name": "z",
                        "filter_limit_min": 0.05,
                        "filter_limit_max": 0.3,
                        # 0.05, 0.3 is ok
                        "filter_limit_negative": False,
                    }
                ],
                remappings=[("input", "/utlidar/cloud_deskewed"), ("output", "/pcl/voxel_grid")],
            ),
            Node(
                package="pcl_ros",
                executable="filter_radius_outlier_removal_node",
                name="filter_radius_outlier_removal_node",
                output="screen",
                parameters=[
                    {
                        "min_neighbors": 3,
                        "radius_search": 0.1,
                        # (4, 0.1) is ok
                    }
                ],
                remappings=[
                    ("input", "/pcl/voxel_grid"),
                    # ("input", "/utlidar/cloud_deskewed"),
                    ("output", "/pcl/outlier_rm"),
                ],
            ),
            # Node(
            #     package="pcl_ros",
            #     executable="filter_statistical_outlier_removal_node",
            #     name="filter_statistical_outlier_removal_node",
            #     output="screen",
            #     parameters=[
            #         {
            #             "mean_k": 50,
            #             "stddev": 0.5,
            #         }
            #     ],
            #     remappings=[("input", "/pcl/voxel_grid"), ("output", "/pcl/outlier_rm")],
            # ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="static_transform_publisher",
                output="screen",
                arguments=["0", "0", "0", "0", "0", "0", "1", "map", "odom"],
            ),
            Node(
                package="octomap_server",
                executable="octomap_server_node",
                name="octomap",
                output="screen",
                # remappings=[("cloud_in", "/pcl/voxel_grid")],
                remappings=[("cloud_in", "/pcl/outlier_rm")],
                # remappings=[("cloud_in", "/utlidar/cloud_deskewed")],
                parameters=[
                    {
                        "frame_id": "odom",
                        "base_frame_id": "odom_rt",
                        "resolution": 0.05,
                        "pointcloud_min_z": 0.1,
                        "pointcloud_max_z": 1.0,
                        "sensor_model": {
                            # "max_range": -1,
                            "hit": 1.0,
                            "miss": 0.45,
                            "max": 1.0,
                            "min": 0.2,
                        },
                    }
                ],
            ),
            # RViz node
            # Node(
            #     package="rviz2",
            #     executable="rviz2",
            #     name="rviz",
            #     arguments=[
            #         "-d",
            #         get_package_share_directory("pcl_ros") + "/samples/pcl_ros/filters/config/default.rviz",
            #     ],
            #     condition=IfCondition(LaunchConfiguration("gui")),
            # ),
        ]
    )
