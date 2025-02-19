from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    passthrough_param = {}
    if 1:
        passthrough_param = {
            "filter_field_name": "intensity",
            "filter_limit_min": 120.0,
            "filter_limit_max": 127.0,
            "filter_limit_negative": False,
        }
    else:
        passthrough_param = {
            "filter_field_name": "z",
            "filter_limit_min": 0.2,
            "filter_limit_max": 0.6,
            "filter_limit_negative": False,
        }
    return LaunchDescription(
        [
            DeclareLaunchArgument("gui", default_value="true", description="Enable GUI"),
            DeclareLaunchArgument("test", default_value="true", description="Run tests"),
            DeclareLaunchArgument("leaf_size", default_value="0.05", description="Voxel grid leaf size"),
            Node(
                package="pcl_ros",
                executable="filter_passthrough_node",
                name="passthrough",
                output="screen",
                parameters=[passthrough_param],
                # remappings=[("input", "/camera/depth/color/points"), ("output", "/pcl/passthrough")],
                remappings=[("input", "/utlidar/cloud_deskewed"), ("output", "/pcl/passthrough")],
            ),
            Node(
                package="pcl_ros",
                executable="filter_voxel_grid_node",
                name="voxel_grid",
                parameters=[{"filter_field_name": "", "leaf_size": LaunchConfiguration("leaf_size")}],
                # remappings=[('input', '/camera/depth/color/points')]
                # remappings=[('input', 'points')]
                remappings=[("input", "/pcl/passthrough"), ("output", "/pcl/voxel_grid")],
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
