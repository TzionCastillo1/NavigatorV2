from dronekit import connect
from navigator_interfaces.srv import VehicleLocation
import rclpy
from rclpy.node import Node


class DronekitService(Node):

        def __init__(self, vehicle):
                super().__init__('dronekit_service')
                self.srv = self.create_service(VehicleLocation, 'vehicle_location', self.vehicle_location_callback)
                self.vehicle = vehicle
                self.get_logger().info('Initializing Dronekit Service ...')
        def vehicle_location_callback(self,request, response):
                #print(type(self.vehicle.location.global_frame.lon))
                #print(self.vehicle.location.global_frame.lon)                response.lon = float(self.vehicle.location.global_frame.lon)
                response.lat = float(self.vehicle.location.global_frame.lat)
                response.spd = float(self.vehicle.location.global_frame.alt)
                response.alt = float(self.vehicle.groundspeed)
                response.dpth = float(self.vehicle.rangefinder.distance)
                self.get_logger().info('Outgoing Data\nlat: %f lon: %f dpth: %f' %(response.lat,response.lon,response.dpth))
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


        
