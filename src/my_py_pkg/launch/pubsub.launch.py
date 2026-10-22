from launch import LaunchDescription
from launch_ros.actions import Node 

def generate_launch_description():

    pub_node = Node(
        package='my_py_pkg',
        executable='pub',
        name='pub_node',
        output='screen'
    )

    sub_node = Node(
        package='my_py_pkg',
        executable='sub',
        name='sub_node',
        output='screen'
    )
    return LaunchDescription([
        pub_node,
        sub_node
    ]
    )
