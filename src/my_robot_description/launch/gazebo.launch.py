from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # Ruta al launch de Gazebo
    gz_sim_launch_file = PathJoinSubstitution([
        FindPackageShare('ros_gz_sim'),
        'launch',
        'gz_sim.launch.py'
    ])

    # Tu mundo
    custom_world = PathJoinSubstitution([
        FindPackageShare('my_robot_description'),
        'worlds',
        'my_prueba_world.sdf'
    ])

    # Lanzar Gazebo con ese mundo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_sim_launch_file),
        launch_arguments={
            'gz_args': ['-r ', custom_world]
        }.items()
    )

    return LaunchDescription([
        gazebo
    ])