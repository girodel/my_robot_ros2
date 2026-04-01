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

    package_name = "my_robot_description"
    robot_name = "my_robot"

    robot_description_path = get_package_share_directory(package_name)

    urdf_file = "my_robot.urdf.xacro"
    rviz_file = "my_robot_gazebo.rviz"
    world_file = "my_custom_world.sdf"

    robot_package = FindPackageShare(package_name)

    parent_of_share_path = os.path.dirname(robot_description_path)

    set_gz_sim_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[os.environ.get("GZ_SIM_RESOURCE_PATH", ""), os.path.pathsep, parent_of_share_path]
    )

    robot_description = ParameterValue(
        Command([
            "xacro ",
            PathJoinSubstitution([robot_package, "urdf", urdf_file])
        ]),
        value_type=str
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            "robot_description": robot_description,
            "use_sim_time": True
        }]
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=[
            "-d",
            PathJoinSubstitution([robot_package, "rviz", rviz_file])
        ],
        parameters=[{"use_sim_time": True}]
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            ])
        ]),
        launch_arguments={
            "gz_args": PathJoinSubstitution([
                "-r ",
                PathJoinSubstitution([robot_package, "worlds", world_file])
            ])
        }.items()
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic", "robot_description",
            "-name", robot_name,
            "-x", "0",
            "-y", "0",
            "-z", "0.02"
        ],
        output="screen"
    )

    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        output="screen",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
            "/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
            "/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",
            "/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry",
            f"/model/{robot_name}/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
            "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist"
        ]
    )

    map_odom_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["0", "0", "0", "0", "0", "0", "1", "map", f"{robot_name}/odom"]
    )

    return LaunchDescription([
        set_gz_sim_resource_path,
        robot_state_publisher,
        gz_sim,
        spawn_robot,
        ros_gz_bridge,
        map_odom_tf,
        rviz
    ])