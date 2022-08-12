import time
import threading
from navigator.csv_handler import CsvPublisher
from navigator_interfaces.srv import VehicleLocation
from navigator_interfaces.srv import WaterParameters
import rclpy
from rclpy.node import Node
import requests

DEVICE_LABEL = "navigator_beta"
TOKEN = "BBFF-HgyKQvO4YreuL5P4WVbQRMe8cCaGVD"

class RepeatedTimer(object):
        def __init__(self,interval,function,*args,**kwargs):
                self.timer = None
                self.interval = interval
                self.function = function
                self.args = args
                self.kwargs = kwargs
                self.is_running = False
                self.next_call = time.time()
                self.start()

        def _run(self):
                self.is_running = False
                self.start()
                self.function(self.args)
        
        def start(self):
                if not self.is_running:
                        self.next_call += self.interval
                        self._timer = threading.Timer(self.next_call - time.time(), self._run)
                        self._timer.start()
                        self.is_running = True

        def stop(self):
                self._timer.cancel()
                self.is_running = False


class DronekitClientAsync(Node):
        def __init__(self):
                super().__init__('dronekit_client_async')
                self.cli = self.create_client(VehicleLocation, 'vehicle_location')
                while not self.cli.wait_for_service(timeout_sec=1.0):
                        self.get_logger().info('service not available, waiting again ...')
                self.get_logger().info('Service available')
                self.req = VehicleLocation.Request()
        def send_request(self):
                self.req.a = 1
                self.future = self.cli.call_async(self.req)


class Y4000ClientAsync(Node):
        def __init__(self):
                super().__init__('y4000_client_async')
                self.cli = self.create_client(WaterParameters, 'water_parameters')
                while not self.cli.wait_for_service(timeout_sec=1.0):
                        self.get_logger().info('service not available, waiting again ...')
                self.req = WaterParameters.Request()
        def send_request(self):
                self.req.a = 1
                self.future = self.cli.call_async(self.req)

class UbidotsPublisher():
        def __init__(self, dk_response, wq_response, token, device_label):
                self.dk_response = dk_response
                self.wq_response = wq_response
                self.token = token
                self.device_label = device_label
                self.payload = {}
                self.build_payload()
                self.post_request()
                
        def build_payload(self):
                fix = True
                isreading = True
                if self.wq_response.temp == 0:
                        isreading = False
                        time.sleep(15)
                        publish()
                        return
                else:
                        self.payload["odo"] = self.wq_response.odo
                        self.payload["turb"] = self.wq_response.turb
                        self.payload["ct"] = self.wq_response.ct
                        self.payload["ph"] = self.wq_response.ph
                        self.payload["temp"] = self.wq_response.temp
                        self.payload["orp"] = self.wq_response.orp
                        self.payload["bga"] = self.wq_response.bga
                        self.payload["dpth"] = self.dk_response.dpth
                if self.dk_response.lat == 0:
                        fix = False
                else:
                        self.payload["position"] = {"value":int(fix), "context": {"lat": self.dk_response.lat, "lng": self.dk_response.lon}}
                

                #self.payload = {"position" : {"value":int(isfix), "context": {"lat": self.dk_response.lat, "lng": self.dk_response.lon}},
                #                "odo" : self.wq_response.odo, "turb" : self.wq_response.turb, "ct" : self.wq_response.ct, "ph" : self.wq_response.ph,
                #                "temp": self.wq_response.temp, "orp" : self.wq_response.orp, "bga" : self.wq_response.bga}
                
        def post_request(self):
                url = "http://industrial.api.ubidots.com"
                url = "{}/api/v1.6/devices/{}".format(url, self.device_label)
                headers = {"X-Auth-Token": self.token, "Content-Type": "application/json"}

                #Make HTTP Request
                status = 400
                attempts = 0
                while status >= 400 and attempts <=5:
                        req = requests.post(url=url, headers=headers, json=self.payload)
                        status = req.status_code
                        attempts += 1
                        time.sleep(1)

                #process results
                print(req.status_code, req.json())
                if status >= 400:
                        print("[ERROR] Could not send data after 5 attempts.")
                        return False
                print("[INFO] request made successfully")
                return True



def publish(csv_publisher):
        rclpy.init(args=None)
        y4000_client = Y4000ClientAsync()
        y4000_client.send_request()
        while rclpy.ok():
                rclpy.spin_once(y4000_client)
                if y4000_client.future.done():
                        try:
                                wq_response = y4000_client.future.result()
                        except Exception as e:
                                y4000_client.get_logger().info('Service call failed %r' %(e,))
                        else:
                                y4000_client.get_logger().info('Result of Data Request:%r' %
                                wq_response)
                        break
        y4000_client.destroy_node()
        dronekit_client = DronekitClientAsync()
        dronekit_client.send_request()
        while rclpy.ok():
                rclpy.spin_once(dronekit_client)
                if dronekit_client.future.done():
                        try:
                                dk_response = dronekit_client.future.result()
                        except Exception as e:
                                dronekit_client.get_logger().info('Service call failed %r' %(e,))
                        else:
                                dronekit_client.get_logger().info('Result of Data Request: Latitude: %r, Longitude: %r, Altitude: %r' %
                                (dk_response.lat, dk_response.lon, dk_response.alt))
                        break
        dronekit_client.destroy_node()
        rclpy.shutdown()
        
        #positionvariables = {'lat':dk_response.lat, 'lon':dk_response.lon, 'alt':dk_response.alt, 'spd':dk_response.spd}
        #dronekit_client.get_logger().info('Variables Received: %s , %s' %(dk_response, wq_response))
        ubidots_publisher = UbidotsPublisher(dk_response,wq_response, TOKEN, DEVICE_LABEL)
        csv_publisher.publish_to_file(dk_response, wq_response)
        #ubidots_publisher.post_request()

def main(args=None):
        csv_publisher = CsvPublisher(DEVICE_LABEL)
        rt = RepeatedTimer(60, publish, args=csv_publisher)
        

if __name__ == '__main__':
        main()
