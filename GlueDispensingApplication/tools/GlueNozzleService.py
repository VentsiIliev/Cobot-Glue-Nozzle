import time
import platform
import minimalmodbus

from GlueDispensingApplication.modbusCommunication.ModbusClientSingleton import ModbusClientSingleton

class GlueNozzleService:
    def __init__(self):
        self.slave = 13

        # # Determine OS and set the correct serial port
        # if platform.system() == "Windows":
        #     self.port = "COM5"  # Adjust as necessary
        # else:  # Assuming Linux
        #     self.port = "/dev/ttyUSB1"  # Adjust as necessary
        #     # self.port = "ttyUSB1"  # Adjust as necessary

        self.port = self.get_modbus_port()

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

    def get_modbus_port(self):
        if platform.system() == "Windows":
            return "COM5"  # Adjust as necessary
        else:  # Assuming Linux
            # Search for USB serial ports
            ports = self.find_usb_ports()
            if ports:
                # Check for the one that matches your Modbus RS485 adapter
                return ports[0]
            else:
                raise Exception("No Modbus RS485 serial ports found!")

    def find_usb_ports(self):
        # List all available USB serial ports
        ports = []
        for port in serial.tools.list_ports.comports():
            if 'USB' in port.description:  # Filter by USB description
                print(f"Found port: {port.device} - {port.description}")
                # You can add more specific filtering based on your device
                # For example, check if the device description matches a known RS485 device
                if "RS485" in port.description or "Modbus" in port.description:
                    ports.append(port.device)
        return ports
