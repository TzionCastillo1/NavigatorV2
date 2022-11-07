from minimalmodbus import Instrument, BYTEORDER_LITTLE
from y4000.spfloat_to_int import float_to_decimal

class Sonde(Instrument):
    #Register addresses for Y4000
    TEMPREG = 0x2606
    DOREG = 0x2601
    TURBREG = 0x2602
    CONDREG = 0x2603
    PHREG = 0x2604
    ORPREG = 0x260B
    CHLREG = 0x260C
    def __init__(self, port, address):
        super().__init__(port, address)
        self.serial.baudrate = 9600
    def read_all_sensors(self):
        sensor_dec = []
        regtoread = [self.DOREG,self.TURBREG, self.CONDREG,self.PHREG,self.TEMPREG,self.ORPREG, self.CHLREG]
        for reg in regtoread:
            sensor_dec.append(self.read_float(reg, byteorder=BYTEORDER_LITTLE))
        return sensor_dec
        
    #Deprecated
    def read_all_sensors_conc(self):
        reg_count = 0
        sensor_count = 0
        sensor_hex = [[],[],[],[],[],[]]
        sensor_dec = []
        values = self.read_registers(0x2601, 0x0C)
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

    #TODO Use error code in ROS2 logging
    def is_error(self):
        error_code = self.read_register(0x0800)
        error_map = {
            0x00: "none",
            0x02: "Humidity Communication",
            0x04: "Voltage Issue",
            0x10: "Sensor is Submerged"
        }
        return error_map.get(error_code, "Code Not Recognized")
    
    