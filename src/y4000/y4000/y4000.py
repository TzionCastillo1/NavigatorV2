from navigator_interfaces.srv import WaterParameters
import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from y4000.y4000_reader import Sonde

class Y4000service(Node):
    def __init__(self):
        super().__init__('y4000_service')
        self.srv = self.create_service(WaterParameters, 'water_parameters', self.water_parameters_callback)
        self.sonde = Sonde('/dev/ttyUSB1',0x01)
        self.get_logger().info('Initializing Y4000 Connection ...')
    def water_parameters_callback(self,request, response):
        try:
            print("working here")
            self.readings = self.sonde.read_all_sensors()
            #self.get_logger().info('Raw Return: %s' (str(self.readings),))
            response.odo = self.readings[0]
            response.turb = self.readings[1]
            response.ct = self.readings[2]
            response.ph = self.readings[3]
            response.temp = self.readings[4]
            response.orp = self.readings[5]
            response.bga = float(-9999)
        except Exception as e:
            self.get_logger().error('Service Return Failed while reading from Sonde %r' %(e,))
        
        return response
def main(args=None):
    rclpy.init(args=args)
    rclpy.logging._root_logger.set_level(LoggingSeverity.DEBUG)
    y4000service = Y4000service()
    try:
        rclpy.spin(y4000service)
    except Exception as e:
        y4000service.get_logger().info('Service Return Failed %r' %(e,))
    rclpy.shutdown()


if __name__ == '__main__':
    main()
