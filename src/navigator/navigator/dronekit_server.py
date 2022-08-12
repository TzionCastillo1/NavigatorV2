from dronekit import connect
from navigator_interfaces.srv import VehicleLocation
import rclpy
from rclpy.node import Node
import time



class DronekitService(Node):

        def __init__(self, vehicle):
                super().__init__('dronekit_service')
                self.srv = self.create_service(VehicleLocation, 'vehicle_location', self.vehicle_location_callback)
                self.vehicle = vehicle
                
                self.get_logger().info('Initializing Dronekit Service ...')
        def get_time_callback(self, attr_name, msg):
                print(msg)
                print(msg.time_usec)
                self.time_usec = msg.time_usec
        def vehicle_location_callback(self,request, response):
                self.time_usec = 0
                #print(type(self.vehicle.location.global_frame.lon))
                #print(self.vehicle.location.global_frame.lon)                
                self.vehicle.add_message_listener('UTM_GLOBAL_POSITION', self.get_time_callback)
                time.sleep(2)
                response.lon = float(self.vehicle.location.global_frame.lon)
                response.lat = float(self.vehicle.location.global_frame.lat)
                response.spd = float(self.vehicle.location.global_frame.alt)
                response.alt = float(self.vehicle.groundspeed)
                response.dpth = float(self.vehicle.rangefinder.distance)
                if self.time_usec == 0:
                        self.get_logger().info('Time from Companion Computer; May not be accurate')
                        self.time_usec = int(time.time() * 1000000)
                response.time_usec = self.time_usec
                
                self.vehicle.remove_message_listener('UTM_GLOBAL_POSITION', self.get_time_callback)
                self.get_logger().info('Outgoing Data:\nlat: %f lon: %f dpth: %f time(usec): %d' %(response.lat,response.lon,response.dpth, response.time_usec))
                return response

def main(args=None):
        rclpy.init(args=args)
        #Connect to Autopilot, Output Error Message if not able to
        try:
                vehicle = connect('/dev/ttyACM1', wait_ready=True, baud=56700)
                dronekit_service = DronekitService(vehicle)
        except Exception as e:
                dronekit_service.get_logger().info('Vehicle Connection Failed %r' %(e,))
        #Spin the ROS2 Service
        try:
                rclpy.spin(dronekit_service)
        except Exception as e:
                dronekit_service.get_logger().info('Service Return Failed %r' %(e,))
        rclpy.shutdown()

if __name__ == '__main__':
        main()


        
