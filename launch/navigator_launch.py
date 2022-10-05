from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
        return LaunchDescription([
                Node(
                        package='navigator',
                        #namespace='navigator',
                        executable='autopilot_interface',
                        #name='navigator'
                ),
                Node(
                        package='y4000',
                        #namespace='y4000',
                        executable='y4000_node',
                        #name='y4000'
                ),
                Node(
                        package='navigator',
                        #namespace='navigator',
                        executable='data_handler',
                        #name='y4000'
                )
        ])