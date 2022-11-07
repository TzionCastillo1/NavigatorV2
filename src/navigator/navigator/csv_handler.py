import csv
from datetime import date
from pathlib import Path
import time

class CsvPublisher():
        def __init__(self, device_label):
                self.device_label = device_label
                self.csv_labels = ['Time', 'Lat', 'Lon', 'Dpth', 'ODO', 'Turb','Ct','pH','Temp','ORP','CHL']
                self.csv_units = ['Seconds from Epoch', 'Degrees', 'Degrees', 'Meters', 'mg/L', 'NTU', 'mS/cm', '', 'Degrees Celsius', 'mV', 'ug/L'] 
                self.create_file()
        def create_file(self):
                #TODO Update file creation system. New file for every time the vehicle is armed?
                Path("logs").mkdir(parents=True, exist_ok=True)
                self.file_name = 'logs/' + self.device_label + str(date.today()) + '.csv'
                try:
                        with open(self.file_name, 'r') as existing_file:
                                return
                except FileNotFoundError:
                        with open(self.file_name, 'w') as new_file:
                                csv_writer = csv.writer(new_file, delimiter=',')
                                csv_writer.writerow(self.csv_labels)
                                csv_writer.writerow(self.csv_units)
        def publish(self, payload):
                new_row = [time.time(), payload["position"]["context"]["lat"], payload["position"]["context"]["lng"], payload["dpth"],
                        payload["odo"], payload["turb"], payload["ct"], payload["ph"], payload["temp"], payload["orp"], payload["chl"]]
                try: 
                        with open(self.file_name, 'a') as file:
                                csv_writer = csv.writer(file, delimiter=',')
                                csv_writer.writerow(new_row)
                except Exception as e:
                        print("Could not write row to file: %r" %(e,))
