import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_diff_drive = get_package_share_directory('diff_drive')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    world_path = os.path.join(pkg_diff_drive, 'worlds', 'diff_drive.sdf')
    xacro_path = os.path.join(pkg_diff_drive, 'urdf', 'diff_drive.urdf.xacro')
    rviz_config = os.path.join(pkg_diff_drive, 'rviz', 'diff_drive.rviz')

    robot_description = xacro.process_file(xacro_path).toxml()

    rviz_arg = DeclareLaunchArgument(
        'rviz', default_value='false',
        description='Start RViz2 alongside Gazebo')

    # 1) Gazebo Fortress with our world (-r = start unpaused)
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world_path}'}.items(),
    )

    # 2) robot_state_publisher: URDF -> /robot_description + TF for fixed joints
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }],
    )

    # 3) Spawn the robot into Gazebo from the /robot_description topic
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'diff_drive',
            '-z', '0.15',
        ],
    )

    # 4) Bridge:  [ = gz -> ROS,  ] = ROS -> gz
    #    We bridge the plugins' default gz topics and remap them to the
    #    standard ROS names (/cmd_vel, /odom, /tf, /joint_states).
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/model/diff_drive/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            '/model/diff_drive/odometry@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/model/diff_drive/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
            '/world/diff_drive_world/model/diff_drive/joint_state@sensor_msgs/msg/JointState[ignition.msgs.Model',
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
        ],
        remappings=[
            ('/model/diff_drive/cmd_vel', '/cmd_vel'),
            ('/model/diff_drive/odometry', '/odom'),
            ('/model/diff_drive/tf', '/tf'),
            ('/world/diff_drive_world/model/diff_drive/joint_state', '/joint_states'),
        ],
        parameters=[{'use_sim_time': True}],
    )

    # 5) Optional RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        condition=IfCondition(LaunchConfiguration('rviz')),
    )

    return LaunchDescription([
        rviz_arg,
        gz_sim,
        robot_state_publisher,
        spawn_robot,
        bridge,
        rviz,
    ])
