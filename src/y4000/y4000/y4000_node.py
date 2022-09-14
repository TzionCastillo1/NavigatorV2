from navigator_interfaces.srv import WaterParameters
import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from y4000.y4000_reader import Sonde
from navigator_interfaces.msg import Y4000_msg

class Y4000Node(Node):
    def __init__(self):
        super().__init__('y4000_node')
        self.publisher = self.create_publisher(Y4000_msg, 'y4000', 10)
        timer_period = 120
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        self.readings = self.sonde.read_all_sensors()
        try:
            msg = Y4000_msg()
            msg.odo = self.readings[0]
            msg.turb = self.readings[1]
            msg.ct = self.readings[2]
            msg.ph = self.readings[3]
            msg.temp = self.readings[4]
            msg.orp = self.readings[5]
        except Exception as e:
            self.get_logger().error('Topic publish failed while reading from Sonde %r' %(e,))


def main(args=None):
    rclpy.init(args=args)
    rclpy.logging._root_logger.set_level(LoggingSeverity.DEBUG)
    y4000 = Y4000Node()
    try:
        rclpy.spin(y4000)
    except Exception as e:
        y4000.get_logger().info('Message publish failed: %r' %(e,))
    rclpy.shutdown()


if __name__ == '__main__':
    main()
