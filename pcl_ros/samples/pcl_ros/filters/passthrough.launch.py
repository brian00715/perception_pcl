from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
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
                remappings=[("input", "/camera/depth/color/points")],
                remappings=[("output", "/pcl/passthrough")],
            )
        ]
    )
