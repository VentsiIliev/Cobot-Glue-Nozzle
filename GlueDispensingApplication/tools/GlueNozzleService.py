import time
import platform
import minimalmodbus

from GlueDispensingApplication.modbusCommunication.ModbusClientSingleton import ModbusClientSingleton

class GlueNozzleService:
    def __init__(self):
        self.slave = 13

        # Determine OS and set the correct serial port
        if platform.system() == "Windows":
            self.port = "COM5"  # Adjust as necessary
        else:  # Assuming Linux
            self.port = "/dev/ttyUSB0"  # Adjust as necessary

        print("Slave:", self.slave)
        print("Port:", self.port)
        self.modbusClient = ModbusClientSingleton.get_instance(slave=self.slave, port=self.port, baudrate=115200,
                                                               bytesize=8, stopbits=1, timeout=0.05)

        # self.modbusClient = ModbusClient(self.slave, 'COM5', 115200, 8, 1, 0.05)

        if self.slave is None:
            raise Exception("Modbus slave not found!")

    def sendCommand(self, data):
        self.modbusClient.writeRegisters(100, data)
        print("Entered Values:", data)

    def startGlueDotsDispensing(self):
        data = [1, 16, 4, 20, 30, 24000, 0, 1800, 0]
        print("Starting glue dots dispensing")
        self.modbusClient.writeRegisters(100, data)

    def startGlueLineDispensing(self):
        data = [1, 16, 4, 20, 30, 24000, 0, 1600, 0]
        print("Starting glue line dispensing")
        self.modbusClient.writeRegisters(100, data)

    def stopGlueDispensing(self):
        print("Stopping glue dispensing")
        self.modbusClient.writeRegister(100, 0)
        print("Stopped glue dispensing")
        # self.modbusClient.writeRegister(101, 4)
