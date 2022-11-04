#ROS2 related imports
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import NavSatStatus
from std_msgs.msg import Header
from navigator_interfaces.msg import ArmStatus, Depth
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
                self.get_logger().info('Initializing Dronekit Service ...')

                self.declare_parameter('operation_mode')
                self.operation_mode = self.get_parameter('operation_mode')
                #self.location_publisher = self.create_publisher(
                #        NavSatFix, 'gps/fix', 10)
                #timer_period = 0.5 # seconds
                self.arm_publisher = self.create_publisher(
                        ArmStatus, 'arm_status', 10)
                self.vehicle = vehicle
                #self.timer = self.create_timer(timer_period, self.timer_callback)
                vehicle.add_message_listener('SYSTEM_TIME', self.listener) 
                vehicle.add_attribute_listener('armed', self.arm_callback)               
                #self.get_logger().info(str(self.operation_mode.value))
                #Check if we are in test mode
                if(str(self.operation_mode.value) == 'TEST'):
                        self.get_logger().info("Running in TEST mode.")
                        vehicle.armed = True
                        while not vehicle.armed:
                                self.get_logger().info(" Waiting")
                                time.sleep(1)
                else:
                        self.get_logger().info("Running in FIELD mode.")


        def timer_callback(self):
                msg = NavSatFix()
                
                msg.header = Header()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = "gps"

                #msg.status.status = NavSatStatus.STATUS_FIX
                #msg.status.service = NavSatStatus.SERVICE_GPS
                #Latitude and Longitude in Decimal Degrees
                msg.latitude = self.vehicle.location.global_frame.lat
                msg.longitude = self.vehicle.location.global_frame.lon
                #Altitude in Meters
                msg.altitude = self.vehicle.location.global_frame.alt

                msg.position_covariance[0] = 0
                msg.position_covariance[4] = 0
                msg.position_covariance[8] = 0
                msg.position_covariance_type = NavSatFix.COVARIANCE_TYPE_DIAGONAL_KNOWN

                dpth_msg = Depth()
                dpth_msg.depth = float(self.vehicle.rangefinder.distance)
                self.location_publisher.publish(msg)
                self.depth_publisher.publish(dpth_msg)
                self.best_pos_a = None
        
        #not sure what 3rd input in this functino is
        def listener(self, name, unsure, msg):
                self.get_logger().info('time(ms from epoch): %i' %(int(msg.time_unix_usec)))
                #print(msg.time_usec)
                self.time_usec = int(msg.time_unix_usec)
                timestamp = datetime.fromtimestamp(self.time_usec / 1000000)
                self.get_logger().info('Time from GPS:%s' %(str(timestamp),))
                timestamp = timestamp.strftime("%Y%m%d %H:%M:%S")
                try:
                        os.system('timedatectl set-ntp false')
                        os.system('sudo date -u --set="%s"' %timestamp)
                except:
                        self.get_logger().info('Cannot set time')
                self.vehicle.remove_message_listener('SYSTEM_TIME', self.listener)

        def arm_callback(self, attr_name, smthng, msg):
                arm_msg = ArmStatus()
                self.get_logger().info('arm message: %s %s' %(msg,type(msg)))
                if(msg == True):
                        arm_msg.armed = True 
                        self.location_publisher = self.create_publisher(
                        NavSatFix, 'gps/fix', 10)
                        self.depth_publisher = self.create_publisher(
                                Depth, 'depth', 10)
                        timer_period = 1
                         # seconds
                        self.timer = self.create_timer(timer_period, self.timer_callback)
                        
                        
                else:
                        arm_msg.armed = False 
                        if(hasattr(self, "location_publisher")):
                                self.destroy_publisher(self.location_publisher)
                                self.destroy_publisher(self.depth_publisher)
                                self.destroy_timer(self.timer)
                self.arm_publisher.publish(arm_msg)

def main(args=None):
        rclpy.init(args=args)
        #Connect to Autopilot, Output Error Message if not able to
        vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=56700)
        #vehicle.add_attribute_listener('utm_global_position', utm_global_position_callback)

        autopilot_node = AutopilotNode(vehicle)  
        
        #Spin the ROS2 Service
        try:
                rclpy.spin(autopilot_node)
        except Exception as e:
                autopilot_node.get_logger().info('publish failed%r' %(e,))
        rclpy.shutdown()

if __name__ == '__main__':
        main()


        
