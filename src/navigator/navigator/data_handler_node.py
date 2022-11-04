import rclpy
from rclpy.node import Node
from navigator_interfaces.msg import Y4000msg, Depth
from sensor_msgs.msg import NavSatFix, NavSatStatus, Image
from std_msgs.msg import Header

from navigator.csv_handler import CsvPublisher
from navigator.ubidots_handler import UbidotsPublisher
import time

DEVICE_LABEL = "navigator_beta"
TOKEN = "BBFF-HgyKQvO4YreuL5P4WVbQRMe8cCaGVD"
class DataHandlerNode(Node):
        def __init__(self):
                self.payload = {}
                self.payload["dpth"] = 0
                self.payload["lastimg"] = 0
                self.lastimgtimer = 0
                self.csv_publisher = CsvPublisher(DEVICE_LABEL)
                self.ubidots_publisher = UbidotsPublisher(TOKEN, DEVICE_LABEL)
                super().__init__('datahandler_node')
                self.y4000Subscriber = self.create_subscription(
                        Y4000msg,
                        'y4000',
                        self.y4000_callback,
                        10
                )
                self.autopilotSubscriber = self.create_subscription(
                        NavSatFix,
                        'gps/fix',
                        self.gps_callback,
                        10
                )
                self.depthSubscriber = self.create_subscription(
                        Depth,
                        'depth',
                        self.depth_callback,
                        10
                )
                self.img_subscriber_ = self.create_subscription(
                        Image, 
                        '/color/image', 
                        self.image_callback, 
                        10
                )

        def y4000_callback(self, message):
                self.get_logger().info('3')
                self.payload["odo"] = message.odo
                self.payload["turb"] = message.turb
                self.payload["ct"] = message.ct
                self.payload["ph"] = message.ph
                self.payload["temp"] = message.temp
                self.payload["orp"] = message.orp
                self.payload["bga"] = message.bga
                #Check if we have received an image in the past 45 seconds
                if(time.perf_counter() - self.lastimgtimer < 45):
                        self.payload["lastimg"] = 1
                else:
                        self.payload["lastimg"] = 0
                try:
                        self.csv_publisher.publish(self.payload)
                except Exception as e:
                        self.get_logger().info('Publish to CSV Failed : %r' %(e,))
                try:
                        self.ubidots_publisher.publish(self.payload)
                except Exception as e:
                        self.get_logger().info('Publish to Ubidots Failed : %r' %(e,))
                self.get_logger().info('4')
                

        def gps_callback(self, message):
                self.get_logger().info('1')
                #self.lat = message.latitude
                #self.lon = message.longitude
                #self.alt = message.altitude
                fix = True
                #if message.latitude == 0: fix = False
                #self.get_logger().info(self.payload)
                self.payload["position"] = {"value":int(fix), "context": {"lat": message.latitude, "lng": message.longitude}}
                self.get_logger().info('2')
                #self.payload["position"]["value"] = int(fix)
                #self.payload["payload"]["context"] = {"lat": message.latitude, "lng": message.longitude}
                #self.get_logger().info('Latitude : %s, \n Longitude : %s, \n Altitude : %s' %(message.latitude,message.longitude,message.altitude))

        def depth_callback(self, message):
                self.payload["dpth"] = message.depth

        def image_callback(self, message):
                self.lastimgtimer = time.perf_counter()

def main(args=None):
        rclpy.init(args=args)
        
        data_handler_node = DataHandlerNode()
        try:
                rclpy.spin(data_handler_node)
        except Exception as e:
                data_handler_node.get_logger().info('subscribe failed %r' %(e,))
        rclpy.shutdown() 

if __name__ == '__main__':
        main()