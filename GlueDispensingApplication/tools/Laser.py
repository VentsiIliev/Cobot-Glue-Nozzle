from GlueDispensingApplication.modbusCommunication.ModbusClient import ModbusClient
from GlueDispensingApplication.modbusCommunication.ModbusClientSingleton import ModbusClientSingleton
import platform

class Laser:
    def __init__(self):
        self.slave = 1

        # Determine OS and set the correct serial port
        if platform.system() == "Windows":
            self.port = "COM5"  # Adjust as necessary
        else:  # Assuming Linux
            self.port = "/dev/ttyUSB0"  # Adjust as necessary

        self.modbusClient = ModbusClient(self.slave, self.port, 115200, 8, 1, 0.05)

    def turnOn(self):
        self.modbusClient.writeRegister(16, 1)
        print("Turning on laser")

    def turnOff(self):
        self.modbusClient.writeRegister(16, 0)
        print("Turning off laser")
