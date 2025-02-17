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
            Node(
                package="pcl_ros",
                executable="filter_passthrough_node",
                name="passthrough",
                output="screen",
                parameters=[
                    {
                        "filter_field_name": "x",
                        "filter_limit_min": 0.1,
                        "filter_limit_max": 1.0,
                        "filter_limit_negative": False,
                    }
                ],
                remappings=[("input", "/camera/depth/color/points"), ("output", "/pcl/passthrough")],
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
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz",
                arguments=[
                    "-d",
                    get_package_share_directory("pcl_ros") + "/samples/pcl_ros/filters/config/default.rviz",
                ],
                condition=IfCondition(LaunchConfiguration("gui")),
            ),
        ]
    )
