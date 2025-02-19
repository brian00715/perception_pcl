from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="pcl_ros",
                executable="filter_voxel_grid_node",
                name="voxel_grid",
                parameters=[
                    {
                        "filter_field_name": "z",
                        "filter_limit_min": 0.0,
                        "filter_limit_max": 99.0,
                        "filter_limit_negative": False,
                        "leaf_size": 0.02,
                    },
                ],
                remappings=[
                    # ("input", "/camera/depth/color/points"),
                    ("input", "/utlidar/cloud_deskewed"),
                    ("output", "/pcl/voxel_grid"),
                ],
            ),
            Node(
                package="pcl_ros",
                executable="filter_radius_outlier_removal_node",
                name="filter_radius_outlier_removal_node",
                output="screen",
                parameters=[
                    {
                        "min_neighbors": 20,
                        "radius_search": 0.1,
                    }
                ],
                remappings=[
                    # ("input", "/pcl/voxel_grid"),
                    ("input", "/utlidar/cloud_deskewed"),
                    ("output", "/pcl/stat_rm"),
                ],
            ),
        ]
    )
