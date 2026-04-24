#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_name = 'my_robot_description'
    robot_pkg = get_package_share_directory(pkg_name)
    robot_package = FindPackageShare(pkg_name)

    robot_name = 'my_robot'

    # 📄 XACRO
    urdf_path = PathJoinSubstitution([
        robot_package,
        'urdf',
        'my_robot.urdf.xacro'
    ])

    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str
    )

    # 🌍 MUNDO
    world_path = PathJoinSubstitution([
        robot_package,
        'worlds',
        'my_prueba_world.sdf'
    ])

    # 🔥 Gazebo Ignition
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments={
            'gz_args': ['-r ', world_path]
        }.items()
    )

    # 🤖 Robot State Publisher
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    # 🚀 Spawn robot (robusto)
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', robot_name,
            '-string', Command(['xacro ', urdf_path]),
            '-x', '0',
            '-y', '0',
            '-z', '0.5'
        ],
        output='screen'
    )

    bridge = Node(
    package='ros_gz_bridge',
    executable='parameter_bridge',
    parameters=[{
        'config_file': os.path.join(robot_pkg, 'config', 'gazebo_bridge.yaml')
    }],
    output='screen'
    )

    return LaunchDescription([

    # 🔥 RUTA PARA RECURSOS (Ignition)
    SetEnvironmentVariable(
    name='GZ_SIM_RESOURCE_PATH',
    value=[
        os.environ.get('GZ_SIM_RESOURCE_PATH', ''),
        os.pathsep,
        os.path.dirname(robot_pkg)  # ✅ CLAVE
    ]
    ),

    # 🔥 ESTA ES LA QUE TE FALTA (MUY IMPORTANTE)
    SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[
            os.environ.get('GAZEBO_MODEL_PATH', ''),
            os.pathsep,
            robot_pkg
        ]
    ),

    gazebo,
    rsp,
    spawn,
    bridge
    ])