import os
from ament_index_python.packages import get_package_share_directory
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('orchard_vehicle_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'vehicle.xacro')
    info_yaml  = os.path.join(pkg_share, 'config', 'vehicle_info.param.yaml')

    doc = xacro.process_file(xacro_file, mappings={'vehicle_info_yaml': info_yaml})
    robot_description = doc.toxml()

    return LaunchDescription([
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}]),
        Node(package='tf2_ros', executable='static_transform_publisher',
             arguments=['0','0','0','0','0','0','map','base_link']),
        Node(package='rviz2', executable='rviz2', output='screen'),
    ])
