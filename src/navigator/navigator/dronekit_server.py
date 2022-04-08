from dronekit import connect
from navigator_interfaces.srv import VehicleLocation
import rclpy
from rclpy.node import Node


class DronekitService(Node):

        def __init__(self, vehicle):
                super().__init__('dronekit_service')
                self.srv = self.create_service(VehicleLocation, 'vehicle_location', self.vehicle_location_callback)
                self.vehicle = vehicle
        def vehicle_location_callback(self,request, response):
                #print(type(self.vehicle.location.global_frame.lon))
                #print(self.vehicle.location.global_frame.lon)
                response.lon = float(0)#float(self.vehicle.location.global_frame.lon)
                response.lat = float(0)#float(self.vehicle.location.global_frame.lat)
                response.spd = float(0)#float(self.vehicle.location.global_frame.alt)
                response.alt = float(0)#float(self.vehicle.groundspeed)
                self.get_logger().info('Outgoing Data\nlat: %f lon: %f' %(response.lat,response.lon))
                return response

def main(args=None):
        vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=56700)
        print(type(vehicle.location.global_frame.lon))
        print(vehicle.location.global_frame.lon)
        rclpy.init(args=args)
        dronekit_service = DronekitService(vehicle)
        try:
                rclpy.spin(dronekit_service)
        except Exception as e:
                dronekit_service.get_logger().info('Service Return Failed %r' %(e,))
        rclpy.shutdown()

if __name__ == '__main__':
        main()


        
