import csv
from datetime import date
from pathlib import Path

class CsvPublisher():
        def __init__(self, device_label):
                self.device_label = device_label
                self.csv_labels = ['Time', 'Lat', 'Lon', 'Dpth', 'ODO', 'Turb','Ct','pH','Temp','ORP','BGA']
                self.create_file()
        def create_file(self):
                Path("logs").mkdir(parents=True, exist_ok=True)
                self.file_name = 'logs/' + self.device_label + str(date.today()) + '.csv'
                try:
                        with open(self.file_name, 'r') as existing_file:
                                return
                except FileNotFoundError:
                        with open(self.file_name, 'w') as new_file:
                                csv_writer = csv.writer(new_file, delimiter=',')
                                csv_writer.writerow(self.csv_labels)
        def publish_to_file(self, dk_response, wq_response):
                new_row = [dk_response.time_usec, dk_response.lat, dk_response.lon,
                        dk_response.dpth, wq_response.odo, wq_response.turb, wq_response.ct,
                        wq_response.ph, wq_response.temp, wq_response.orp, wq_response.bga]
                try: 
                        with open(self.file_name, 'a') as file:
                                csv_writer = csv.writer(file, delimiter=',')
                                csv_writer.writerow(new_row)
                except Exception as e:
                        print("Could not write row to file: %r" %(e,))