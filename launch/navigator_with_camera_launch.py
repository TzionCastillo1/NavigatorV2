from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():
        operation_mode          = LaunchConfiguration('operation_mode', default="FIELD")

        declare_operation_mode_cmd = DeclareLaunchArgument(
                'operation_mode',
                default_value=operation_mode,
                description='The operation mode of the Navigator. Using the `FIELD` mode enables checks for GPS fix. Using the `TEST` mode disables the GPS fix check. Valid modes: `FIELD, TEST`.'
                )
        autopilot_node = Node(
                package='navigator',
                #namespace='navigator',
                executable='autopilot_interface',
                parameters = [{'operation_mode': operation_mode}]
                #name='navigator'
        )
        y4000_node = Node(
                package='y4000',
                #namespace='y4000',
                executable='y4000_node',
                #name='y4000'
        )
        data_handler_node = Node(
                package='navigator',
                #namespace='navigator',
                executable='data_handler',
                #name='y4000'
        )
        img_saver_node = Node(
                package = 'navigator_img_saver',
                executable='img_saver',
                parameters = [{'operation_mode': operation_mode}]
        )
        
        ld = LaunchDescription()
        ld.add_action(declare_operation_mode_cmd)
        ld.add_action(autopilot_node)
        ld.add_action(y4000_node)
        ld.add_action(data_handler_node)
        ld.add_action(img_saver_node)
        return ld