#ROS2 related imports
from navigator_interfaces.srv import VehicleLocation
from navigator.navigator_class import Navigator
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import NavSatStatus
from std_msgs.msg import Header
import rclpy
from rclpy.node import Node
#Other imports
from dronekit import connect
import time
import os
from datetime import datetime


class AutopilotNode(Node):
        def __init__(self, vehicle):
                super().__init__('Autopilot')
                self.location_publisher = self.create_publisher(
                        NavSatFix, 'gps/fix', 10)
                timer_period = 0.5 # seconds
                self.vehicle = vehicle
                self.timer = self.create_timer(timer_period, self.timer_callback)
        def timer_callback(self):
                msg = NavSatFix
                msg.header = Header()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = "gps"

                msg.status.status = NavSatStatus.STATUS_FIX
                msg.status.service = NavSatStatus.SERVICE_GPS
                #Latitude and Longitude in Decimal Degrees
                msg.latitude = self.vehicle.location.global_frame.lat
                msg.longitude = self.vehicle.location.global_frame.lon
                #Altitude in Meters
                msg.altitude = self.vehicle.location.global_frame.alt

                msg.position_covariance[0] = 0
                msg.position_covariance[4] = 0
                msg.position_covariance[8] = 0
                msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN

                self.location_publisher.publish(msg)
                self.best_pos_a = None

def main(args=None):
        rclpy.init(args=args)
        #Connect to Autopilot, Output Error Message if not able to
        vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=56700, vehicle_class=Navigator)
        vehicle.add_attribute_listener('utm_global_position', utm_global_position_callback)

        autopilot_node = AutopilotNode  
        
        #Spin the ROS2 Service
        try:
                rclpy.spin(autopilot_node)
        except Exception as e:
                autopilot_node.get_logger().info('publish failed%r' %(e,))
        rclpy.shutdown()

if __name__ == '__main__':
        main()


        
