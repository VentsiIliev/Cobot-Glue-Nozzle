from GlueDispensingApplication.modbusCommunication.ModbusClient import ModbusClient
from GlueDispensingApplication.modbusCommunication.ModbusClientSingleton import ModbusClientSingleton
import platform
import subprocess
import re  # Import regex module

class Laser:
    def __init__(self):
        self.slave = 1

        # Determine OS and set the correct serial port
        if platform.system() == "Windows":
            self.port = "COM5"  # Adjust as necessary
        else:  # Assuming Linux
            # self.port = "/dev/ttyUSB0"  # Adjust as necessary
            self.port = self.find_ch341_uart_port()  # Adjust as necessary

        self.modbusClient = ModbusClient(self.slave, self.port, 115200, 8, 1, 0.05)

    def turnOn(self):
        self.modbusClient.writeRegister(16, 1)
        print("Turning on laser")

    def turnOff(self):
        self.modbusClient.writeRegister(16, 0)
        print("Turning off laser")

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
