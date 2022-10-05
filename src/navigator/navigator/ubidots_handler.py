from datetime import date
import requests
import time


class UbidotsPublisher():
        def __init__(self,token, device_label):
                self.token = token
                self.device_label = device_label

        def publish(self, payload):
                url = "http://industrial.api.ubidots.com"
                url = "{}/api/v1.6/devices/{}".format(url, self.device_label)
                headers = {"X-Auth-Token": self.token, "Content-Type": "application/json"}

                #Make HTTP Request
                status = 400
                attempts = 0
                while status >= 400 and attempts <=5:
                        req = requests.post(url=url, headers=headers, json=payload)
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

