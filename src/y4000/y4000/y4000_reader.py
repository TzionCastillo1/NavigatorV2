from minimalmodbus import Instrument
from y4000.spfloat_to_int import float_to_decimal

class Sonde(Instrument):
    
    def __init__(self, port, address):
        super().__init__(port, address)
        self.serial.baudrate = 9600
    def read_all_sensors(self):
        values = self.read_registers(0x2601, 0x0C)
        reg_count = 0
        sensor_count = 0
        sensor_hex = [[],[],[],[],[],[]]
        sensor_dec = []
        for value in values:
            if reg_count < 1:
                value = hex(value)
                byte_1 = value[2] + value[3]
                byte_2 = value[4] 
                if len(value) == 6:
                    byte_2 += value[5]
                sensor_hex[sensor_count].append(int(byte_1, base=16))
                sensor_hex[sensor_count].append(int(byte_2, base=16))
                reg_count +=1
            else:
                value = hex(value)
                byte_1 = value[2] + value[3]
                byte_2 = value[4] 
                if len(value) == 6:
                    byte_2 += value[5]
                sensor_hex[sensor_count].append(int(byte_1, base=16))
                sensor_hex[sensor_count].append(int(byte_2, base=16))
                reg_count = 0
                sensor_count+=1
        for sensor in sensor_hex:
            #decimal = float_to_decimal(sensor)
            sensor_dec.append(float_to_decimal(sensor))
        return sensor_dec 

    def is_error(self):
        error_code = self.read_register(0x0800)
        error_map = {
            0x00: "none",
            0x02: "Humidity Communication",
            0x04: "Voltage Issue",
            0x10: "Sensor is Submerged"
        }
        return error_map.get(error_code, "Code Not Recognized")
    
    