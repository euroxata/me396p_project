import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_name = 'padwq'
    pkg_share_dir = FindPackageShare(pkg_name) 

    default_robot_name = 'padwq'

    # set launch arguments
    robot_name = LaunchConfiguration('robot_name')
    use_rsp = LaunchConfiguration('use_rsp')
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_jsp_gui = LaunchConfiguration('use_jsp_gui')
    use_rviz = LaunchConfiguration('use_rviz')
    use_controller = LaunchConfiguration('use_controller')

    robot_name_arg = DeclareLaunchArgument(
        name='robot_name',
        default_value=default_robot_name,
        description='absolute path to the robot urdf file'
    )

    use_rsp_arg = DeclareLaunchArgument(
        name='use_rsp',
        default_value='True',
        description='flag to start the robot state publisher'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='False',
        description='flag to use the simulation (Gazebo) clock'
    )

    use_jsp_gui_arg = DeclareLaunchArgument(
        name='use_jsp_gui',
        default_value='True',
        description='flag to enable GUI of the joint state publisher'
    )

    use_rviz_arg = DeclareLaunchArgument(
        name='use_rviz',
        default_value='True',
        description='flag to start RVIZ'
    )
    
    use_controller_arg = DeclareLaunchArgument(
        name='use_controller',
        default_value='False',
        description='flag to start PADWQ controller'
    )

    # define nodes
    robot_state_publisher_node = Node(
        condition=IfCondition(use_rsp),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'use_sim_time': use_sim_time, 
            'robot_description': Command([
                'xacro ',
                PathJoinSubstitution([pkg_share_dir, robot_name]),
                '.urdf'
            ])
        }]
    )

    joint_state_publisher_node = Node(
        condition=UnlessCondition(use_jsp_gui),
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    joint_state_publisher_gui_node = Node(
        condition=IfCondition(use_jsp_gui),
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    rviz_node = Node(
        condition=IfCondition(use_rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', 
                [
                    PathJoinSubstitution([pkg_share_dir, robot_name]),
                    '.rviz'
                ]
        ]
    )

    controller_node = Node(
        condition=IfCondition(use_controller),
        package='padwq',
        executable='controller',
        name='controller'
    )

    ld = LaunchDescription([
                               robot_name_arg,
                               use_rsp_arg,
                               use_sim_time_arg,
                               use_jsp_gui_arg,
                               use_rviz_arg,
                               use_controller_arg,
                               robot_state_publisher_node,
                               joint_state_publisher_node,
                               joint_state_publisher_gui_node,
                               rviz_node,
                               controller_node
                           ])

    return ld
