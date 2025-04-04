import time
import minimalmodbus


class ModbusClient:
    def __init__(self, slave=10, port='COM5', baudrate=115200, bytesize=8, stopbits=1, timeout=0.01):
        self.slave = slave
        self.client = minimalmodbus.Instrument(port, self.slave, debug=False)
        # self.client1 = minimalmodbus.Instrument('COM5', self.slave, debug=False)
        # self.client1 = minimalmodbus.Instrument('COM16', self.slave, debug=False)
        # self.client1 = minimalmodbus.Instrument('/dev/ttyUSB0', 10, debug=False)

        # if self.client1.serial.is_open:
        #     self.client1.serial.close()

        self.client.serial.baudrate = baudrate
        self.client.serial.bytesize = bytesize
        self.client.serial.stopbits = stopbits
        self.client.serial.timeout = timeout
        self.client.serial.parity = minimalmodbus.serial.PARITY_NONE

    def writeRegister(self, register, value):
        maxAttempts = 30
        attempts = 0
        while attempts < maxAttempts:
            try:
                print("Writing value to modbus: ", value)
                self.client.write_register(register, value)
                break
            except minimalmodbus.ModbusException as e:
                if "Checksum error in rtu mode" in str(e):
                    print(f"Modbus Exception: {e}.")
                    break
                print(f"Modbus Exception: {e}")
                attempts += 1
                # time.sleep(0.1)

    def writeRegisters(self, start_register, values):
        maxAttempts = 30
        attempts = 0
        while attempts < maxAttempts:
            try:
                print("Writing values to modbus: ", values)
                self.client.write_registers(start_register, values)
                break
            except minimalmodbus.ModbusException as e:
                if "Checksum error in rtu mode" in str(e):
                    print(f"Modbus Exception: {e}")
                    break
                print(f"Modbus Exception: {e}")
                attempts += 1
                # time.sleep(0.1)

