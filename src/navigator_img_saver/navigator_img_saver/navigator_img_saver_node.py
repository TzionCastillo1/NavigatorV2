#Node to listen to images published, and save for future CV use
#after a distance or time interval has passed

#Importing the necessary libraries
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, NavSatFix, NavSatStatus
import cv2
from cv_bridge import CvBridge

#from haversine import haversine, Unit

class ImageSaverNode(Node):
        def __init__(self):
                super().__init__('img_svr_node')
                self.img_subscriber_ = self.create_subscription(Image, '/color/image', self.image_callback, 10)
                self.gps_subscriber = self.create_subscription(
                        NavSatFix,
                        'gps/fix',
                        self.gps_callback,
                        10
                )
                self.br = CvBridge()
                self.lat = 0
                self.lon = 0
                self.img_flag = False
        def image_callback(self, msg):
              if(self.img_flag):
                current_frame = self.br.imgmsg_to_cv2(msg)
                cv2.imwrite(self.tuple_to_string(self.coord),current_frame)

        def gps_callback(self, msg):
                if(self.lat == 0):
                        self.coord = (tuple) (msg.latitude, msg.longitude)
                else:
                        self.last_coord = (tuple) (msg.latitude, msg.longitude)
                        #if(haversine(self.coord, self.last_coord, unit = Unit.METERS) > 5 ):
                        #        self.img_flag = True
                        #        self.coord = self.last_coord

        def tuple_to_string(self, tup):
                str = ''.join(tup)
                return str
                
def main(args=None):
        rclpy.init(args=args)
        image_saver_node = ImageSaverNode()

        #Spin Subscription
        try:
                rclpy.spin(image_saver_node)
                image_saver_node.get_logger().info('Subscription sucssessful')
        except Exception as e:
                image_saver_node.get_logger().info('Subscriber Creation Failed %r' %(e,))

        

if __name__ == '__main__':
        main()