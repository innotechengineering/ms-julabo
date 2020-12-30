#!/usr/bin/env python3
import serial

#standard python logging
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Julabo(object):
    def __init__(self):
        self.sc = serial.Serial(port='/dev/ttyUSB0',
                                baudrate=4800,
                                bytesize=serial.SEVENBITS,
                                parity=serial.PARITY_EVEN,
                                stopbits=serial.STOPBITS_ONE,
                                timeout=5,
                                xonxoff=False,                   # software flow control
                                rtscts=True,                    # enable hardware (RTS/CTS) flow control
                                write_timeout=None,              
                                dsrdtr=True,                     # enable hardware (DSR/DTR) flow control
                                inter_byte_timeout=None,
                                exclusive=None)
        self.sc.reset_input_buffer()
        self.sc.reset_output_buffer()

    def close(self):
        self.sc.close()

    def rs232_control(self): 
        # command to set the Diamond into rs232 control
        self.sc.write("**REMOTE".encode('utf-8'))
        print(self.sc.readline())  # may need to clear the input buffer is the julabo responds here ???

    def dump_datalog(self):
        self.sc.write("**DATALOGGER_OUT".encode('utf-8'))
        # TODO - loop through reads here to drain datalog memeory - not sure yet

    def _write_then_read(self, strToSend):
        self.sc.write(strToSend.encode('utf-8'))
        resp = self.sc.readline().strip().decode('utf-8')
        return resp

    def read_version(self):
        return self._write_then_read("version\r")

    def read_status(self):
        return self._write_then_read("status\r")

    def read_bath_temp(self):
        return self._write_then_read("in_pv_00\r")

    def read_heating_power(self):
        return self._write_then_read("in_pv_01\r")

    def read_pt100(self):
        return self._write_then_read("in_pv_02\r")

    def read_saftey_sensor(self):
        return self._write_then_read("in_pv_03\r")
    
    def read_working_temp(self):
        return self._write_then_read("in_sp_00\r")

    def read_temp_units(self):
        return self._write_then_read("IN_SP_06\r")

    def read_circulator_status(self):
        return self._write_then_read("in_mode_05\r")

    def start_circulator(self):
        return self._write_then_read("out_mode_05 1\r")

    def stop_circulator(self):
        return self._write_then_read("out_mode_05 0\r")

    def set_working_temp(self, setTemp):
        """for now, setTemp should be a string xxx.xx"""
        return self._write_then_read("out_sp_00 " + setTemp + '\r')

if __name__ == "__main__":
    julabo = Julabo()
    #julabo.rs232_control()
    ver = julabo.read_version()
    print(f"Version: {ver}")
    print(f"Status: {julabo.read_status()}")
    circulatorStates = ["STOPPED", "RUNNING"]
    circulatorStatus = circulatorStates[int(julabo.read_circulator_status())]
    print(f"Circulator status: {circulatorStatus}")
    tempUnits = ["C", "F"]
    tempUnits = tempUnits[int(julabo.read_temp_units())]
    print(f"Working temp (setpoint): {julabo.read_working_temp()}{tempUnits}")
    bathTemp = julabo.read_bath_temp()
    print(f"Actual Bath temp: {bathTemp}{tempUnits}")
    heatingPower = julabo.read_heating_power()
    print(f"Heating power: {heatingPower}%")
    print()
    print(f"Saftey sensor: {julabo.read_saftey_sensor()}{tempUnits}")


    
    julabo.close()
