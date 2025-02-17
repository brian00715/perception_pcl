from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'gui',
            default_value='true',
            description='Enable GUI'
        ),
        DeclareLaunchArgument(
            'test',
            default_value='true',
            description='Run tests'
        ),
        DeclareLaunchArgument(
            'leaf_size',
            default_value='0.05',
            description='Voxel grid leaf size'
        ),

        # PCD to PointCloud node
        Node(
            package='pcl_ros',
            executable='pcd_to_pointcloud',
            name='pcd_to_pointcloud',
            parameters=[{
                'file_name': get_package_share_directory('pcl_ros') + '/samples/data/table_scene_lms400.pcd',
                'interval': 0.033
            }],
            remappings=[('cloud_pcd', 'points')]
        ),

        # Voxel Grid node
        Node(
            package='pcl_ros',
            executable='filter_voxel_grid_node',
            name='voxel_grid',
            parameters=[{
                'filter_field_name': '',
                'leaf_size': LaunchConfiguration('leaf_size')
            }],
            remappings=[('input', 'points')]
        ),

        # RViz node
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz',
            # arguments=['-d', get_package_share_directory('pcl_ros') + '/samples/pcl_ros/filters/config/voxel_grid.rviz'],
            condition=IfCondition(LaunchConfiguration('gui'))
        ),

        # 注意：ROS2的测试框架需要单独配置，这里需要根据实际测试需求进行调整
        # ROS2的launch测试框架与ROS1不同，建议使用launch_testing框架创建单独的测试文件
    ])