from navigator_interfaces.srv import WaterParameters
import rclpy
from rclpy.node import Node
from rclpy.logging import LoggingSeverity
from y4000.y4000_reader import Sonde
from navigator_interfaces.msg import Y4000msg, ArmStatus
from std_msgs.msg import Header
class Y4000Node(Node):
    def __init__(self):
        super().__init__('y4000_node')
        #self.publisher = self.create_publisher(Y4000msg, 'y4000', 10)
        #timer_period = 70
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        self.sonde = Sonde('/dev/ttyUSB0',0x01)
        self.attempts = 0
        self.armedstateSubscriber = self.create_subscription(
            ArmStatus,
            'arm_status',
            self.arm_callback,
            10
        )

    def timer_callback(self):
        try:
            self.readings = self.sonde.read_all_sensors()
            msg = Y4000msg()
            msg.header = Header()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = "Y4000"
            msg.odo = self.readings[0]
            msg.turb = self.readings[1]
            msg.ct = self.readings[2]
            msg.ph = self.readings[3]
            msg.temp = self.readings[4]
            msg.orp = self.readings[5]
            #self.attempts = 0
            self.publisher.publish(msg)
            self.attempts = 0
        except Exception as e:
            self.get_logger().error('Topic publish failed while reading from Sonde %r' %(e,))
            if(self.attempts > 3) : 
                self.attempts += 1
                self.timer_callback()

    def arm_callback(self, message):
        if(message.armed == True):
            self.publisher = self.create_publisher(Y4000msg, 'y4000', 10)
            timer_period = 70
            self.timer = self.create_timer(timer_period, self.timer_callback)
        else:
            if(hasattr(self, "publisher")):
                self.destroy_publisher(self.publisher)
                self.destroy_timer(self.timer)


                



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
