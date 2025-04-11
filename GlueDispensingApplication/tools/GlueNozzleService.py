import time
import platform
import minimalmodbus
import subprocess
import re

from GlueDispensingApplication.modbusCommunication.ModbusClientSingleton import ModbusClientSingleton

class GlueNozzleService:
    def __init__(self):
        self.slave = 13
        self.port = self.get_modbus_port()

        print("Slave:", self.slave)
        print("Port:", self.port)
        self.modbusClient = ModbusClientSingleton.get_instance(slave=self.slave, port=self.port, baudrate=115200,
                                                               bytesize=8, stopbits=1, timeout=0.05)

        if self.slave is None:
            raise Exception("Modbus slave not found!")

    def sendCommand(self, data):
        self.modbusClient.writeRegisters(100, data)
        print("Entered Values:", data)

    def startGlueDotsDispensing(self):
        data = [1, 16, 4, 20, 30, 24000, 0, 3000, 0]
        print("Starting glue dots dispensing")
        self.modbusClient.writeRegisters(100, data)

    def startGlueLineDispensing(self):
        data = [1, 16, 4, 20, 30, 24000, 0, 3000, 0]
        print("Starting glue line dispensing")
        self.modbusClient.writeRegisters(100, data)

    def stopGlueDispensing(self):
        print("Stopping glue dispensing")
        self.modbusClient.writeRegister(100, 0)
        print("Stopped glue dispensing")

    def get_modbus_port(self):
        if platform.system() == "Windows":
            return "COM5"  # Adjust as necessary
        else:  # Assuming Linux
            port = self.find_ch341_uart_port()
            if port:
                return port
            else:
                raise Exception("No Modbus 485 serial ports found!")

    def find_ch341_uart_port(self):
        # Run dmesg with sudo to fetch system log
        password = "123"  # Set the password here
        result = subprocess.run(
            ["sudo", "-S", "dmesg"], input=password + "\n", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Check for 'ch341-uart' using regex to extract the ttyUSB device (e.g., ttyUSB0, ttyUSB1, etc.)
        pattern = r'ch341-uart.*?ttyUSB(\d+)'  # Regex to match 'ch341-uart' and extract 'ttyUSB0', 'ttyUSB1', etc.

        # Reverse the output to get the most recent device first
        lines = result.stdout.splitlines()
        lines.reverse()  # Reverse the order of lines to check the most recent logs first

        for line in lines:
            if "now attached" in line:  # Check if "now attached" is in the line
                print("line: ",line)
                if re.search(pattern, line):  # If a match for the pattern is found
                    # Extract the ttyUSB device from the matched line
                    match = re.search(pattern, line)
                    if match:
                        device = f"/dev/ttyUSB{match.group(1)}"
                        print("Device: ",device)# Extract the number from the regex match
                        return device

        return None  # If no match is found


if __name__ == "__main__":
    service = GlueNozzleService()
