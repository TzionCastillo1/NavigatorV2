from dronekit import connect
from navigator_interfaces.srv import VehicleLocation
import rclpy
from rclpy.node import Node
vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=56700)


class DronekitService(Node):

        def __init__(self):
                super().__init__('dronekit_service')
                self.srv = self.create_service(VehicleLocation, 'vehicle_location', self.vehicle_location_callback)
                #self.vehicle = vehicle
        def vehicle_location_callback(self,request, response):
                global vehicle
                print("1")
                #print(type(self.vehicle.location.global_frame.lon))
                #print(self.vehicle.location.global_frame.lon)
                response.lon = vehicle.location.global_frame.lon
                response.lat = vehicle.location.global_frame.lat
                response.spd = vehicle.location.global_frame.alt
                response.alt = vehicle.groundspeed
                #self.get_logger().info('Outgoing Data\nlat: %f lon: %f' %(response.lat,response.lon))
                return response

def main(args=None):
        print(type(vehicle.location.global_frame.lon))
        print(vehicle.location.global_frame.lon)
        rclpy.init(args=args)
        print("2")
        dronekit_service = DronekitService()
        print("3")
        try:
                rclpy.spin(dronekit_service)
                print("4")
        except Exception as e:
                print("5")
                dronekit_service.get_logger().info('Service Return Failed %r' %(e,))
        rclpy.shutdown()

if __name__ == '__main__':
        main()


        
