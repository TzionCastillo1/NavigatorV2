import rclpy
from rclpy.node import Node
from navigator_interfaces.msg import Y4000_msg
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import NavSatStatus
from std_msgs.msg import Header

from resource.csv_handler import CsvPublisher
from resource.ubidots_handler import UbidotsPublisher


DEVICE_LABEL = "navigator_beta"
TOKEN = "BBFF-HgyKQvO4YreuL5P4WVbQRMe8cCaGVD"
class DataHandlerNode(Node):
        def __init__(self):
                super().__init__('datahandler_node')
                self.y4000Subscriber = self.create_subscription(
                        Y4000_msg,
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

        def y4000_callback(self, message):
                self.payload["odo"] = self.message.odo
                self.payload["turb"] = self.message.turb
                self.payload["ct"] = self.message.ct
                self.payload["ph"] = self.message.ph
                self.payload["temp"] = self.message.temp
                self.payload["orp"] = self.message.orp
                self.payload["bga"] = self.message.bga

                CsvPublisher.publish_to_file(self.payload)
                UbidotsPublisher.publish
                

        def gps_callback(self, message):
                #self.lat = message.latitude
                #self.lon = message.longitude
                #self.alt = message.altitude
                if message.latitude == 0: fix = False
                self.payload["position"] = {"value":int(fix), "context": {"lat": message.latitude, "lng": message.longitude}}
                self.get_logger().info('Latitude : %s, \n Longitude : %s, \n Altitude : %s' %(self.lat,self.lon,self.alt))

        def depth_callback(self, message):
                self.payload["dpth"] = self.dk_response.dpth

def main(args=None):
        csv_publisher = CsvPublisher(DEVICE_LABEL)
        ubidots_publisher = UbidotsPublisher(TOKEN, DEVICE_LABEL)


if __name__ == '__main__':
        main()